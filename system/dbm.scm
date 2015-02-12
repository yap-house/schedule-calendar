#!/usr/local/bin/gosh

(use dbm.fsdbm)

(define-macro db (make-parameter #f))

(define-syntax with-db
  (syntax-rules ()
    ((with-db (db path) . body)
     (parameterize ((db (dbm-open <fsdbm> :path path :rw-mode :write)))
                   (with-error-handler (lambda (e) (dbm-close (db)) (raise e))
                                       (lambda ()
                                         (begin0
                                          (begin . body)
                                          (dbm-close (db)))))))))

(define-macro (dbm-key-start y m d) #`",|y|-,|m|-,|d|-start")
(define-macro (dbm-key-end y m d) #`",|y|-,|m|-,|d|-end")
(define-macro (dbm-key-total y m d) #`",|y|-,|m|-,|d|-total")
(define-macro (dbm-key-comment y m d) #`",|y|-,|m|-,|d|")

(define-macro (data-exists key) (dbm-exists? (db) key))

(define-macro (get-data key) (dbm-get (db) key ""))

(define-macro (put-data key val) (dbm-put! (db) key val))

(define-macro (delete-data key) (dbm-delete! (db) key))

(define-macro (set-data key val)
  (if (string-null? val)
      (delete-data key) (put-data key val)))

