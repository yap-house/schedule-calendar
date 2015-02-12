#!/usr/local/bin/gosh

(require "./config")
(require "loader")

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
       (html:p y)))))
(main "")

