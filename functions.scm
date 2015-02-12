#!/usr/local/bin/gosh

(define (add-load-path path)
  (set! *load-path* (append *load-path* (list path))))


;; calendar functions

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
