
function is_numeric(str) {
    // console.log(str);
    return /^\d+$/.test(str);
}

$(document).ready(function() {

    $("header.navbar-fixed-top").autoHidingNavbar({
        showOnBottom: false
    });

    $('.show_hide').click(function() {
        $("#filters-content").slideToggle();
    });

    $('.dropdown-menu').find('form').click(function(e) {
        e.stopPropagation();
    });

    $.fn.dataTable.moment( 'DD-MM-YYYY HH:mm' );

    $('#data-table').DataTable({
        'pageLength': DATATABLE_PAGE_SIZE,
        'dom': "Bfrtip",
        fixedHeader: {
            header: true,
            footer: true
        },
        'buttons': [
            {   extend: 'excelHtml5',
                title: 'таблица',
                text: 'Экспортировать в Excel (.xlsx)'  },
            {   extend: 'print',
                title: '',
                text: 'распечатать'  },
            {   text: 'Добавить',
                    action: function (e, dt, node, config) {
                         $('#passwd').val('');
                        $('#myModal').modal({ "show": true });

                        $('#save-btn').click(function(e) {
                            var me = $(this);
                            e.preventDefault();

                            if (me.data('requestRunning')) {
                                return;
                            }

                            me.data('requestRunning', true);
                            var form = $("#add-new-item");

                            $.ajax({
                                type: "POST",
                                url: form.attr("action"),
                                data: form.serialize(),
                                success: function(response) {
                                    // console.log(response);
                                    setTimeout(function() {
                                        location.reload();
                                    }, 1000);
                                },
                                error: function(XMLHttpRequest, textStatus, errorThrown) { 
                                    console.log(errorThrown);
                                    // alert("Status: " + textStatus);
                                    // alert("Error: " + errorThrown); 
                                },
                                complete: function() {
                                    me.data('requestRunning', false);
                                }
                            });
                        });
                    } }
        ],
        'columnDefs': [
            { 'targets': "no-sort", orderable: false }     // 'targets' - указывает на имя css-класса для тегов <th> таблицы.
        ],
        'order': [[ 0, "desc" ]],                          // 'order' - задает номер колонки <th> (нумерация с нуля), по которой делается начальная default-сортировка
        'language': {
            'url': "https://cdn.datatables.net/plug-ins/1.10.13/i18n/Russian.json",
        }
    });

    var table = $('#data-table').DataTable();

    $(window).scroll(function() {
        var scrollh = $(this).scrollTop();
        if (scrollh == 0) {
            // $('.navbar').css({'height': '50px', });
            $('.navbar').removeClass("scrolled");
        }
        else {
            // $(".navbar").css({'height': '30px', });
            $('.navbar').addClass("scrolled");
        }

        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
    });

    // scroll body to 0px on click
    $('#back-to-top').click(function() {
        $('#back-to-top').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });

    // $('#back-to-top').tooltip('show');

    $('#genpass-btn').click(
        function(e) {
            e.preventDefault();
            var password = $.passGen();
            $('#passwd').val(password);
            return;
        }
    );

    $('#login-name').on('blur', function() {
        $('#save-btn').prop('disabled', true);
        var login_name = $('#login-name').val();
        if (login_name == '') {
            return;
        }
        else {
            if (!is_numeric(login_name)) {
                alert("Логин должен быть числовым.");
                return;
            }
            else
                $.ajax({
                    url: '/check_login_exists',
                    type: 'post',
                    data: { 'login_name': login_name },
                    success: function(response) {
                        // console.log(response);
                        json_data = $.parseJSON(response);
                        // console.log(json_data.status);
                        if (json_data.status == false)
                            $('#save-btn').prop('disabled', false);
                        else {
                            $('#save-btn').prop('disabled', true);
                            alert("Пользователь с таким логином уже существует.");
                        }
                    }
                });
        }
    });

    $(".clickable-row").click(function() {
        $("#data-table tbody tr").removeClass('row_selected');
        $(this).addClass('row_selected');

        var url = $(this).data("href");
        $('#modal-detail-body').load(url, function(result) {
            $('#detailModal').modal({ "show": true });
        });
    });
});
