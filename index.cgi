#!/usr/local/bin/gosh

;(require "./config")
;(require "loader")

;(define (main args)
;  (cgi-main
;   (lambda (params)
;     (cgi-output-character-encoding 'utf-8)
;     (with-db (db *db-name*)
;              (cmd-show-calendar 2015 2)))))

(use text.html-lite)
(use www.cgi)

(define (main args)
  (cgi-main
    (lambda (params)
      `(,(cgi-header)
        ,(html-doctype)
        ,(html:html
          (html:head (html:title "Example"))
          (html:body
           (html:table
            :border 1
            (html:tr (html:th "Name") (html:th "Value"))
            (map (lambda (p)
                   (html:tr
                    (html:td (html-escape-string (car p)))
                    (html:td (html-escape-string (x->string (cdr p))))))
                 params))))
       ))))

;(define (main args)
;  (cgi-main
;   (lambda (params)
;     (let ((y (cgi-get-parameter "y" params :convert x->integer))
;           (m (cgi-get-parameter "m" params :convert x->integer))
;           (d (cgi-get-parameter "d" params :convert x->integer))
;           (status (cgi-get-parameter "status" params))
;           (start (cgi-get-parameter "start" params
;                                     :convert (cut ces-convert <> "*jp")))
;           (end (cgi-get-parameter "end" params
;                                   :convert (cut ces-convert <> "*jp")))
;           (total (cgi-get-parameter "total" params
;                                     :convert (cut ces-convert <> "*jp")))
;           (comment (cgi-get-parameter "comment" params
;                                       :convert (cut ces-convert <> "*jp"))))
;
;       (cgi-output-character-encoding 'utf-8)
;
;       (with-db (db *db-name*)
;                (if (and y m d)
;                    (cond
;                     ((equal? status "e")
;                      (cmd-edit-report y m d))
;                     ((equal? status "c")
;                      (cmd-change-report y m d start end total comment))
;                     (else
;                      (cmd-show-report y m d)))
;                    (cmd-show-calendar y m)))))))
;
;

