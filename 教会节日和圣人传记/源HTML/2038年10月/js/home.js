$(document).ready(function() {
    $('#label-refresh').click(function() {
        $.ajax({
            url: '/api.php?op=get_news&m=labels&count=10',
            type: 'GET',
            success: function(response) {
                $('#label-random-list').empty();
                $(response).each(function() {
                    $('#label-random-list').append('<a href="/index.php?m=news&c=tag&a=lists&tagid=' + this.id + '" target="_blank" class="btn btn-outline-main">' + this.name + '</a>');
                });
            }
        });
    });
});

