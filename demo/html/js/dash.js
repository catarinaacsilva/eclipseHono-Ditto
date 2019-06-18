function setupHighcharts() {
  Highcharts.setOptions({global: {useUTC: false}});
  var ctemp = Highcharts.chart('chartTemp', {
    chart: {type: 'spline'},
    title: {text: 'Temperature'},
    xAxis: {type: 'datetime',tickPixelInterval: 150},
    yAxis: [{min: 0,max: 100,labels: {format: '{value}°C',style: {color: '#f15c80'}},
      title: {text: 'Temperature',style: {color: '#f15c80'}}}],
    legend: {enabled: false},
    exporting: {enabled: false},
    series: [{name: 'Temperature',
      type: 'spline',
      yAxis: 0,
      color: '#f15c80',
      data: (function () {
        var data = [], time = 0, i;
        for (i = 0; i < 10; i += 1) {
          data.push({x: (time - ((10-i) * 1000)),y: 15});
        }
        return data;
      }())
    }]
  });

  var gaugeOptions = {
    chart: {type: 'solidgauge'},
    title: {text: 'RPM'},
    pane: {
      center: ['50%', '85%'],
      size: '140%',
      startAngle: -90,
      endAngle: 90,
      background: {
        backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
        innerRadius: '60%',
        outerRadius: '100%',
        shape: 'arc'
      }
    },
    tooltip: {enabled: false},
    // the value axis
    yAxis: {
      stops: [
        [0.1, '#3D9970'],  // olive
        [0.25, '#2ECC40'], // green
        [0.5, '#FFDC00'],  // yellow
        [0.75, '#FF851B'], // orange
        [0.9, '#FF4136']   // red
      ],
      lineWidth: 0,
      minorTickInterval: null,
      tickPixelInterval: 400,
      tickWidth: 0,
      title: {
        y: -70
      },
      labels: {
        y: 16
      }
    },

    plotOptions: {
      solidgauge: {
        dataLabels: {
          y: 5,
          borderWidth: 0,
          useHTML: true
        }
      }
    }
  };

  var crpm = Highcharts.chart('chartRPM', Highcharts.merge(gaugeOptions, {
    yAxis: {
      min: 0,
      max: 5000,
      title: {text: ''}},
      credits: {enabled: false},
      series: [{
        name: 'rpm',
        data: [0],
        dataLabels: {
          format: '<div style="text-align:center"><span style="font-size:25px;color:' +
            ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
            '<span style="font-size:12px;color:silver">RPM</span></div>'
        },
        tooltip: {
          valueSuffix: 'degree C'
        }
      }]
  }));

  return [ctemp, crpm];
}

function setupWS(charts, ws) {
  var ctemp = charts[0], crpm = charts[1];
  var ws = new WebSocket(ws);
  
  ws.onopen = function()
  {
    console.log("Subscribe events");
    ws.send("START-SEND-EVENTS");
  };

  ws.onmessage = function (evt)
  {
    var received_msg = evt.data;
    console.log(received_msg);
    var json = JSON.parse(received_msg);
    if(json != null) {
      var ts = new Date(json.timestamp).getTime();
      var temp = json.value.temperature.properties.value;
      var rpm = json.value.rpm.properties.value;
      ctemp.series[0].addPoint([ts, temp], true, true);
      crpm.series[0].points[0].update(rpm);
    switch(json.topic) {

      case "temperature":
        cbme.series[0].addPoint([ts, json.value], true, true);
        break;
      case "humidity":
        cbme.series[1].addPoint([ts, json.value], true, true);
        break;
      case "pressure":
        cbme.series[2].addPoint([ts, json.value], true, true);
        break;
      case "light":
        cbh.series[0].points[0].update(json.value);
        break;
    }}
  };

  ws.onclose = function()
  {
    console.log("Connection is closed...");
  };
}

function setup(ws) {
  setupWS(setupHighcharts(), ws);  
}
