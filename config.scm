#!/usr/local/bin/gosh

(require "./functions")

(define *style* "static/style.css")

(add-load-path "./system" #t)
(define *calendar* "./calendar/")
(define *views* "./views/")
(display *system*)
