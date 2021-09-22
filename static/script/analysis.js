function imageDetect(select){
        console.log("함수 호출 성공")
//        var select = $(this);
        var src = $(select).attr('src');
        console.log(src)
        $.ajax({
            type: 'POST',
            url: '/analyze',
            data: {
                "src": src
            },
            success: function (results) {
                const side = document.querySelector('#left-side-bar');
                side.classList.add('hide');
                $("#gallery").empty();
                $("#flower_table").empty();
                $("#button_buy").empty();
                $("#myChart").remove();
                $('#phonenum').empty();
                // 디텍션 결과 이미지 출력
                $("#image_container").empty();
                $("#image_container").append(
                    `<img style="width: 640px; height: 480px;" id="thum-img" src="${src}_box.png">`
                )
                // 디텍션 결과 꽃 리스트 출력
                $("#result_detection").empty();
                $("#result_detection").append(
                    `<select id="flower-detect" size=6>
                        <option value="">---꽃 선택---</option>
                    </select>`
                )
                for (let i = 0; i < results.length; i++) {
                    $("#flower-detect").append(
                        `<option id="option-flower" value=${results[i]} onclick="imageAnalyse()">${results[i]}</option>`
                    )
                }

                // 유저 의견 반영 팝업 버튼
                $("#button_container").empty();
                $("#button_container").append(
                        '<input type="button" value="원하시는 결과가 나오지 않으셨나요?" onclick="showPopup()" />'
                )
            }
        })
    }
    function openGallery(){

    }

    function imageDetect2() {
            let fileValue = $("#input-image").val().split("\\");
            var formDataRaw = $('#ImageSelect2')[0];
            var form_data = new FormData(formDataRaw);
            let flowerPoom
            let flowerGood
            $("#flower_table").empty();
            $("#button_buy").empty();
            $("#myChart").remove()
            $('#phonenum').empty()
            $.ajax({
                type: 'POST',
                url: '/image_detect',
                data: form_data,
                contentType: false, // 해당 타입을 true로 하면 일반 text
                cache: false,
                processData: false, // 데이터 객체를 문자열로 바꿀지에 대한 값, true면 일반문자
                async: false,       // 비동기 여부
                success: function(results) {
                    console.log(typeof(results))
                    console.log(results)
                    const side = document.querySelector('#left-side-bar');
                    side.classList.add('hide');
                    // 디텍션 결과 이미지 출력
                    $("#image_container").empty();
                    $("#image_container").append(
                        `<img style="width: 640px; height: 480px;" id="thum-img" src="../../static/img/${fileValue[2]}_box.png">`

                    )
                    // 디텍션 결과 꽃 리스트 출력
                    $("#result_detection").empty();
                    $("#result_detection").append(
                        `<select id="flower-detect" size=6>
                            <option value="">---꽃 선택---</option>
                        </select>`
                    )
                    for (let i = 0; i < results.length; i++) {
                        $("#flower-detect").append(
                            `<option id="option-flower" value=${results[i]} onclick="imageAnalyse()">${results[i]}</option>`
                        )
                    }

                    // 유저 의견 반영 팝업 버튼
                    $("#button_container").empty();
                    $("#button_container").append(
                            '<input type="button" value="원하시는 결과가 나오지 않으셨나요?" onclick="showPopup()" />'
                        )
                }
            })
        }
    // 선택한 꽃 분석
    function imageAnalyse() {
        let flowerValue = $("#flower-detect option:selected").val();
        let flowerPoom
        let flowerGood
        $('#phonenum').empty();
        $.ajax({
            type: "GET",
            url: "/analyse_result?flower_name=" + flowerValue,
            data:{},
            // 성공 시 DB 값 가져와서 테이블 생성
            success: function(results) {
                console.log(flowerValue)
                console.log("분석 결과")

                // table 비우기
                $("#flower_table").empty();
                // table 하위 요소 추가
                $("#flower_table").append(
                    `<!-- 테이블 헤드 -->
                    <thead>
                        <tr>
                            <th>선택</th>
                            <th>품목</th>
                            <th>품종</th>
                            <th>등급</th>
                            <th>속수량</th>
                            <th>낙찰금액</th>
                            <th>입고날짜</th>
                        </tr>
                    </thead>
                    <!-- 테이블 목록(DB 필요) -->
                    <tbody id="flower-list">
                    </tbody>
                    `
                )
                // tbody 하위 요소 추가
                for (let i = 0; i < results.length; i++) {
                    let flower = results[i];
                    $("#flower-list").append(
                        `<tr>
                            <td><input type="checkbox" name="flower-checkbox" onclick="checkOnlyOne(this)"></td>
                             <td>${flower["poomname"]}</td>
                            <td>${flower["goodname"]}</td>
                            <td>${flower["lvname"]}</td>
                            <td>${flower["qty"]}</td>
                            <td>${flower["cost"]}</td>
                            <td>${flower["dateinfo"]}</td>
                        </tr>`
                    )
                    flowerPoom = flower["poomname"]
                    flowerGood = flower["goodname"]
                }
                // 구매 버튼
                $("#button_buy").empty();
                $("#button_buy").append(
                    `
                    <select name="fl_shop" id="fl_shop">
                        <option value="하나 도매장터">하나 도매장터</option>
                        <option value="정연 플라워즈">정연 플라워즈</option>
                        <option value="The 윤수's">The 윤수's</option>
                    </select>
                    <input type="number" id="flower-quantity" name="flower-quantity" min="1">
                    <input type="button" class="btn btn-warning" value="구매" onClick="buyFlower()">`
                )
                // 그래프 비우기
                $("#myChart").remove()
                $("#chart_container").append(
                    `<canvas id="myChart"></canvas>`
                )
                // 그래프 그리기
                var ctx = document.getElementById("myChart").getContext("2d");
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [
                            {
                                label: "최고가격",
                                fill: false,
                                lineTension: 0.1,
                                backgroundColor: "skyblue",
                                borderColor: "skyblue"
                            },
                            {
                                label: "최저가격",
                                fill: false,
                                lineTension: 0.1,
                                backgroundColor: "pink",
                                borderColor: "pink"
                            },
                            {
                                label: "평균가격",
                                fill: false,
                                lineTension: 0.1,
                                backgroundColor: "gray",
                                borderColor: "gray"
                            }
                        ]
                    },
                    options: {
                        tooltips: {
                            mode: 'index',
                            intersect: false
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero:true
                                }
                            }]
                        }
                    }
                });

                var data = data || {};
                console.log(flowerPoom + "_" + flowerGood + " 그래프 그리기")

                // 가져온 DB 값과 json 파일명 대조하여 그래프 그리기
                // examine example_data.json for expected response data
                var json_url = '/static/json/' + flowerPoom + '_' + flowerGood + '.json'
                console.log(json_url)
                if (json_url !='/static/json/undefined_undefined.json'){

                    $.getJSON(json_url, data).done(function(response) {
                        myChart.data.labels = response.labels;
                        myChart.data.datasets[0].data = response.data.max; // or you can iterate for multiple datasets
                        myChart.data.datasets[1].data = response.data.min;
                        myChart.data.datasets[2].data = response.data.avg;
                        myChart.update(); // finally update our chart
                    });
                }else{
                    $("#flower_table").empty();
                    $("#button_buy").empty();
                    $("#myChart").remove();
                    $('#phonenum').empty();
                    $('#phonenum').append('가격정보가 존재하지 않습니다. 010-7777-7777로 문의주시기 바랍니다.');
                }
            }
        })
    }
    // 체크박스 체크된 꽃 구매
    function buyFlower() {
        var checkbox = $("input[name=flower-checkbox]:checked");
        var qty = $("#flower-quantity").val()
        var shop = $("#fl_shop option:selected").val()
        // 체크된 체크박스 값을 가져온다
        checkbox.each(function(i) {

            // checkbox.parent() : checkbox의 부모는 <td>
            // checkbox.parent().parent() : <td>의 부모이므로 <tr>
            var tr = checkbox.parent().parent().eq(i);
            var td = tr.children();

            // td.eq(0)은 체크박스, td.eq(1)의 값부터 가져온다
            var poomName = td.eq(1).text()
            var goodName = td.eq(2).text()
            var lvName = td.eq(3).text()
            var cost = td.eq(5).text()


            console.log("품목 : " + poomName);
            console.log("품종 : " + goodName);
            console.log("등급 : " + lvName);
            console.log("가격 : " + cost);

            $.ajax({
                url: "/kakaopay/paymethod.ajax",
                data: {
                    poomName: poomName,
                    goodName: goodName,
                    lvName: lvName,
                    qty: qty,
                    cost: cost,
                    shop: shop
                },
                dataType: "json",
                type: "post",
                async: false,
                statusCode: {
                    404: function () {
                        alert("네트워크가 불안정합니다. 다시 시도부탁드립니다.");
                    }
                },
                success: function (data) {
                    location.href=data["next_url"]
                }
            })
        });
    }
    // 체크박스 하나만 선택되도록
    function checkOnlyOne(element) {
        const checkboxes = document.getElementsByName("flower-checkbox");

        checkboxes.forEach((cb) => {
            cb.checked = false;
        })
        element.checked = true;
    }