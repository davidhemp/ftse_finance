
$(function()
{
    var ticker = function()
    {
        setTimeout(function(){
            $('#newsticker li:first').animate( {marginTop: '-120px'}, 800, function()
            {
                $(this).detach().appendTo('ul#newsticker').removeAttr('style');
            });
            ticker();
        }, 4000);
    };
    ticker();
});
