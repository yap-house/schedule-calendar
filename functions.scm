#!/usr/local/bin/gosh

(define (add-load-path path . parm)
  (define mode (:optional parm #f))
  (set! *load-path* (if mode
                        (append *load-path* (list path))
                        (cons path *load-path*))))
