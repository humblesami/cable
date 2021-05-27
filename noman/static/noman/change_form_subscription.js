$(function(){
    if(!document.querySelector('#subscription_form select[name="sale_object"]'))
    {
        return;
    }
    document.querySelector('#subscription_form select[name="sale_object"]').onchange=function() {
        let sale_object_id = this.value;
        let el_due_amount = $('#subscription_form input[name="installment"]');
        if(!sale_object_id){
            el_due_amount.val(0);
            return;
        }
        let options = {
            beforeSend: function(a, b){
                //console.log(b.url);
            },
            url: '/sale_object/charges',
            data : {sale_object_id: sale_object_id},
            success:function(data){
                el_due_amount.val(data);
            },
            error:function(er){
                console.log(er);
            }
        };
        $.ajax(options);
    }
});
name="sale_object"