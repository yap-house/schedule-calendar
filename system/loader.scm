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

(require "./dbm")
(require "./cmb")
(require "../views/index")
(require "../calendar/calendar")
