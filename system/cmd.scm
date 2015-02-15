#!/usr/local/bin/gosh

(define (cmd-show-calendar y m)
  (page
   (if (and y m (<= 1 m 12) (<= 1753 y))
       (calendar (make-month m y))
       (calendar (current-date)))))

(define (cmd-show-report y m d)
  (require "view-show-report")
  (view-show-report y m d))


(define (cmd-edit-report y m d)
  (require "view-edit-report")
  (view-edit-report y m d))


(define (cmd-change-report y m d start end total comment)
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


