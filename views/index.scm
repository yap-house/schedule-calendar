#!/usr/local/bin/gosh

(require "./view-show-calendar")
(require "./view-show-report")
(require "./view-edit-report")

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
