#!/usr/local/bin/gosh

(define (view-edit-report start end total comment)
  (page
   (html:h2 #`",|y|年,|m|月,|d|日の日報 - 編集画面")
   (html:form :method "get" :action "./calendar.cgi"
              (html:input :type "hidden" :name "status" :value "c")
              (html:input :type "hidden" :name "y" :value (x->string y))
              (html:input :type "hidden" :name "m" :value (x->string m))
              (html:input :type "hidden" :name "d" :value (x->string d))

              (html:dl :class "edit"
                       (html:dt "出勤:")
                       (html:dd (html:input :type "text" :name "start"
                                            :value (html-escape-string (get-data start))))
                       (html:dt "退勤:")
                       (html:dd (html:input :type "text" :name "end"
                                            :value (html-escape-string (get-data end))))
                       (html:dt "勤務時間:")
                       (html:dd (html:input :type "text" :name "total"
                                            :value (html-escape-string (get-data total))))
                       (html:dt "コメント:")
                       (html:dd (html:textarea :row 8 :cols 40 :name "comment"
                                               (html-escape-string (get-data comment)))))
              (html:p (html:input :type "submit" :name "submit" :value "更新")))))
