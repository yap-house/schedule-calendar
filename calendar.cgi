#!/usr/local/bin/gosh

(use util.list)
(use srfi-1)
(use srfi-13)
(use srfi-19)
(use text.html-lite)
(use www.cgi)
(use gauche.sequence)
(use gauche.charconv)
(use gauche.parameter)
(use dbm.fsdbm)

(define db (make-parameter #f))
(define *db-name* "data")
(define *style* "static/style.css")


(define-syntax with-db
  (syntax-rules ()
    ((with-db (db path) . body)
     (parameterize ((db (dbm-open <fsdbm> :path path :rw-mode :write)))
                   (with-error-handler (lambda (e) (dbm-close (db)) (raise e))
                                       (lambda ()
                                         (begin0
                                          (begin . body)
                                          (dbm-close (db)))))))))

(define (dbm-key-start y m d) #`",|y|-,|m|-,|d|-start")
(define (dbm-key-end y m d) #`",|y|-,|m|-,|d|-end")
(define (dbm-key-total y m d) #`",|y|-,|m|-,|d|-total")
(define (dbm-key-comment y m d) #`",|y|-,|m|-,|d|")

(define (data-exists key) (dbm-exists? (db) key))
(define (get-data key) (dbm-get (db) key ""))
(define (put-data key val) (dbm-put! (db) key val))
(define (delete-data key) (dbm-delete! (db) key))
(define (set-data key val)
  (if (string-null? val)
      (delete-data key) (put-data key val)))


(define (make-month m y)
  (make-date 0 0 0 0 1 m y (date-zone-offset (current-date))))


(define (first-day-of-month date)
  (make-month (date-month date) (date-year date)))


(define (next-month date)
  (if (= (date-month date) 12)
      (make-month 1 (+ (date-year date) 1))
      (make-month (+ (date-month date) 1) (date-year date))))


(define (prev-month date)
  (if (= (date-month date) 1)
      (make-month 12 (- (date-year date) 1))
      (make-month (- (date-month date) 1) (date-year date))))


(define (days-of-month date)
  (inexact->exact
   (- (date->modified-julian-day (next-month date))
      (date->modified-julian-day (first-day-of-month date)))))


(define (date-slices-of-month date)
  (slices
   (append
    (make-list
     (date-week-day (first-day-of-month date)) #f)
    (iota (days-of-month date) 1))
   7 #t #f))


(define (month->link date content)
  (html:a :href #`"?y=,(date-year date)&m=,(date-month date)" content))


(define (date-cell y m d)
  (if d
      (html:a :href #`"?y=,|y|&m=,|m|&d=,|d|" d
              (if (data-exists (dbm-key-start y m d)) (html:span :class "start" #`"出勤: ,(get-data (dbm-key-start y m d))") "")
              (if (data-exists (dbm-key-end y m d)) (html:span :class "end" #`"退勤: ,(get-data (dbm-key-end y m d))") "")
              (if (data-exists (dbm-key-total y m d)) (html:span :class"total" #`"勤務時間: ,(get-data (dbm-key-total y m d))") ""))
      ""))


(define (calendar date)
  (let ((current-year (date-year date))
        (current-month (date-month date))
        (prev-month (prev-month date))
        (next-month (next-month date)))

    `(,(html:div :class "calendar-header"
                 (html:ul
                  (html:li :class "prev-month"
                           (month->link prev-month #`"&lt; ,(date-year prev-month)/,(date-month prev-month)"))

                  (html:li :class "current-month"
                           #`",|current-year|/,|current-month|")

                  (html:li :class "next-month"
                           (month->link next-month #`",(date-year next-month)/,(date-month next-month) &gt;"))))

      ,(html:table :class "calendar"
                   (html:tr (map html:th "日月火水木金土"))
                   (map (lambda (w)
                          (html:tr
                           (map (lambda (d)
                                  (html:td (date-cell current-year current-month d)))
                                w)))
                        (date-slices-of-month date))))))


(define (page . content)
  `(,(cgi-header)
    ,(html-doctype)
    ,(html:html
      (html:head
       (html:meta :name "viewport" :content "width=device-width")
       (html:meta :http-equiv "Content-Type" :content "text/html; charset=UTF-8")
       (html:title "個別日報管理表")
       (html:link :rel "stylesheet" :href *style*))
      (apply html:body
             (html:h1
              (html:span (html:a :href "./" "個別日報管理表")))
             (html:div :class "wrapper" content)))))


(define (cmd-show-calendar y m)
  (page
   (if (and y m (<= 1 m 12) (<= 1753 y))
       (calendar (make-month m y))
       (calendar (current-date)))))


(define (cmd-show-plan y m d)
  (let
      ((start (dbm-key-start y m d))
       (end (dbm-key-end y m d))
       (total (dbm-key-total y m d))
       (comment (dbm-key-comment y m d)))

    (page
     (html:h2 #`",|y|年,|m|月,|d|日の日報" (html:a :href #`"?y=,|y|&m=,|m|&d=,|d|&status=e" "[予定を編集]"))
     (html:dl :class "report"
              (html:dt "開始時間:")
              (html:dd (html-escape-string (get-data start)))
              (html:dt "終了時間:")
              (html:dd (html-escape-string (get-data end)))
              (html:dt "勤務時間:")
              (html:dd (html-escape-string (get-data total)))
              (html:dt "コメント:")
              (html:td (html-escape-string (get-data comment)))))))


(define (cmd-edit-plan y m d)
  (let
      ((start (dbm-key-start y m d))
       (end (dbm-key-end y m d))
       (total (dbm-key-total y m d))
       (comment (dbm-key-comment y m d)))

    (page
     (html:h2 #`",|y|年,|m|月,|d|日の日報 - 編集画面")
     (html:form :method "get" :action "./calendar.cgi"
                (html:input :type "hidden" :name "status" :value "c")
                (html:input :type "hidden" :name "y" :value (x->string y))
                (html:input :type "hidden" :name "m" :value (x->string m))
                (html:input :type "hidden" :name "d" :value (x->string d))

                (html:dl :class "edit"
                         (html:dt "開始時間:")
                         (html:dd (html:input :type "text" :name "start"
                                              :value (html-escape-string (get-data start))))
                         (html:dt "終了時間:")
                         (html:dd (html:input :type "text" :name "end"
                                              :value (html-escape-string (get-data end))))
                         (html:dt "勤務時間:")
                         (html:dd (html:input :type "text" :name "total"
                                              :value (html-escape-string (get-data total))))
                         (html:dt "コメント:")
                         (html:dd (html:textarea :row 8 :cols 40 :name "comment"
                                                 (html-escape-string (get-data comment)))))
                (html:p (html:input :type "submit" :name "submit" :value "更新"))))))


(define (cmd-change-plan y m d start end total comment)
  (let
      ((key-start (dbm-key-start y m d))
       (key-end (dbm-key-end y m d))
       (key-total (dbm-key-total y m d))
       (key-comment (dbm-key-comment y m d)))

    (set-data key-start start)
    (set-data key-end end)
    (set-data key-total total)
    (set-data key-comment comment)

    (cgi-header :status "302 Moved"
                :location #`"?y=,|y|&m=,|m|&d=,|d|")))

(define (main args)
  (cgi-main
   (lambda (params)
     (let ((y (cgi-get-parameter "y" params :convert x->integer))
           (m (cgi-get-parameter "m" params :convert x->integer))
           (d (cgi-get-parameter "d" params :convert x->integer))
           (status (cgi-get-parameter "status" params))
           (start (cgi-get-parameter "start" params
                                     :convert (cut ces-convert <> "*jp")))
           (end (cgi-get-parameter "end" params
                                     :convert (cut ces-convert <> "*jp")))
           (total (cgi-get-parameter "total" params
                                     :convert (cut ces-convert <> "*jp")))
           (comment (cgi-get-parameter "comment" params
                                       :convert (cut ces-convert <> "*jp"))))

       (cgi-output-character-encoding 'utf-8)
       (with-db (db *db-name*)
                (if (and y m d)
                    (cond
                     ((equal? status "e")
                      (cmd-edit-plan y m d))
                     ((equal? status "c")
                      (cmd-change-plan y m d start end total comment))
                     (else
                      (cmd-show-plan y m d)))
                    (cmd-show-calendar y m)))))))
