document.addEventListener('DOMContentLoaded', function () {
    "use strict";

    const reservationWrapper = document.querySelector('.confirm_requests');
    const dateFormatter = {
        format: 'Y-m-d H:m'
    };

    $('#startimepicker').datetimepicker(
        dateFormatter
    );
    $('#endtimepicker').datetimepicker(
        dateFormatter
    );

    function formateDate(date) {
        let dd = date.getDate();
        if (dd < 10) dd = '0' + dd;

        let mm = date.getMonth() + 1;
        if (mm < 10) mm = '0' + mm;

        let yy = date.getFullYear();

        let hh = date.getHours();
        if (hh < 10) hh = '0' + hh;

        let m = date.getMinutes();
        if (m < 10) m = '0' + m;

        return `${dd}.${mm}.${yy} ${hh}:${m}`;
    }

    function clickBtn(event) {
        event.stopPropagation();
        const clicked = event.target;
        if (clicked.hasAttribute('data-url')) {
            fetchData(clicked.getAttribute('data-url'), function (data) {
                console.log(data);
            });
            reloadRequests();
            reservationWrapper.removeEventListener('click', clickBtn);
        }
    }

    function fetchData(url, dataSuccess) {
        $.ajax({
            url: url,
            type: 'post',
            datatype: 'json',
            success: function (data) {
                dataSuccess(data);
            }
        })
        ;
    }

    function reservingRequestData(data) {
        let newItemlist = document.createElement('ul');
        newItemlist.classList.add('confirm');
        if (data.length > 0) {
            data.forEach(function (item) {
                let newLiItem = document.createElement("li");
                newLiItem.classList.add('confirm__item');
                newLiItem.innerHTML = `<p class="room__title">${item.fields.room.title}</p>
                    <p class="room__time">${formateDate(new Date(item.fields.start_meeting_time))} - ${formateDate(new Date(item.fields.end_meeting_time))}</p>
                    <div class="confirm__btn">
                        <button class="btn btn-success" data-url="/confirm-request/${item.pk}/">Подтвердить</button>
                        <button class="btn btn-danger" data-url="/cancel-request/${item.pk}/">Отказать</button>
                    </div>`;

                newItemlist.appendChild(newLiItem);
            });
            reservationWrapper.replaceChild(newItemlist, reservationWrapper.children[0]);
            reservationWrapper.addEventListener('click', clickBtn);
        } else {
            reservationWrapper.innerHTML = '<p class="center mt-20">Заявок нет</p>';
        }
    }

    function reloadRequests() {
        fetchData('/load-requests/', reservingRequestData);
    }

    if (reservationWrapper !== null) {
        reservationWrapper.addEventListener('click', clickBtn);
        const intevalHandler = setInterval(reloadRequests, 10000);
    }
});
