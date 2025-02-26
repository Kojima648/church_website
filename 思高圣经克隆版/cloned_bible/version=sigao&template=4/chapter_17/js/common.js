function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}
$(document).ready(function () {
    updateWechatShare();
    $(document).on("change.gaoerjun","#top_phone_nav_select",function(){
        window.doChageTopNav &&  window.doChageTopNav($(this));
    })
    $("#top_phone_nav_select").on()
    var offset = 220;
    var duration = 850;
    $(window).scroll(function () {
        if ($(this).scrollTop() > offset) {
            $('.elevator-top').fadeIn(duration);
        } else {
            $('.elevator-top').fadeOut(duration);
        }
    });

    $('.elevator-top').click(function (event) {
        event.preventDefault();
        $('html,body').animate({scrollTop: 0}, duration);
        return false;
    });
    var pathname = location.pathname;
    var mValue = getQueryString("m");
    var pathkey = pathname;
    if(mValue){
        pathkey +="?m="+mValue;
    }
    var currentLi = $("#top_header_nav a[href*='"+pathkey+"']").eq(0).parent("li");
    currentLi.addClass("active").siblings().removeClass("active");
    currentLi.parents("li").addClass("active");

    if($(".flexslider").length>0 && $(".flexslider").flexslider){
        $(".flexslider").flexslider({
            pauseOnAction: true,
            animation: "slide",
            directionNav: false,
            animationLoop: true,
            controlNav: true,
            slideshow: true,
            slideshowSpeed: 5000,
            animationDuration: 500
        });
    }

});
