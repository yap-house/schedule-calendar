#!/usr/local/bin/gosh

(use dbm.fsdbm)

(define db (make-parameter #f))

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
