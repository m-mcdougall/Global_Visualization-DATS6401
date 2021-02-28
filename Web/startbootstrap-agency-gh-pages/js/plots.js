
google.charts.load('current', {'packages':['corechart', 'geochart', 'controls'],
                    'mapsApiKey': 'AIzaSyBoVxauKlXr5UIbGZzMpsao8hc8haGG64Y'});
google.charts.setOnLoadCallback(drawAllSheets);
window.addEventListener('resize', drawAllSheets, false);

function drawAllSheets() {
    drawSheetName ('Dashboard_HEAL', 'SELECT A,B,C,D,E,F,G,H,I,J,K,L', drawDashboard_health);
    drawSheetName ('MIL_HEAL', 'SELECT A,B,C,D,E', drawDashboard_health_mil);
    drawSheetName ('Bubble_HEAL', 'SELECT A,B,C,D,E,F', drawDashboard_health_bubble_gdp);
    drawSheetName ('Line_Change_HEAL', 'SELECT A,B,C,D,E,F,G,H,I,J,K,L', drawLineHealthDashboard);
    drawSheetName ('Global_HEAL', 'SELECT A,B,D', drawGeoDashboard);

    drawSheetName ('Dashboard_EDU', 'SELECT A,B,C,D,E,F,G,H,I,J,K,L', drawDashboard_edu);
    drawSheetName ('MIL_EDU', 'SELECT A,B,C,D,E', drawDashboard_edu_mil);
    drawSheetName ('Bubble_EDU', 'SELECT A,B,C,D,E,F', drawDashboard_edu_bubble_gdp);
    drawSheetName ('Line_Change_EDU', 'SELECT A,B,C,D,E,F,G,H,I,J,K,L', drawLineEduDashboard);
    drawSheetName ('Global_EDU', 'SELECT A,B,D', drawGeoDashboardEdu);


} //drawAllSheetsS
function drawSheetName(sheetName, query, responseHandler){
    var queryString = encodeURIComponent(query);
    var query = new google.visualization.Query(
        //'https://docs.google.com/spreadsheets/d/19XH4jbKGMJS6aarHaSE-1GISPpuA377jl5GwWM7XTYU/gviz/tq?sheet=' https://drive.google.com/file/d/1rb9KEi3taCpDfZBQdvmKIid_wajd41H0/view?usp=sharing
        'https://docs.google.com/spreadsheets/d/14ci-qTkZPHL_xw3WNseAGdjWO95bxErs6bHLBPW0a_M/gviz/tq?sheet='
        + sheetName +'&headers=1&tq=' + queryString );

    query.send(responseHandler)    
}//drawSheetName



function drawDashboard_health(response) {
    var data = response.getDataTable();
    

    console.log(data)
   
    //First Control wrapper  - Filters by Category of Data
    var namePicker = new google.visualization.ControlWrapper({
      'controlType': 'CategoryFilter',
      'containerId': 'filter_div',
      'options': {
        'filterColumnLabel': 'Type',
        'ui': {
          'label': 'Spending Representation',
          'labelStacking': 'vertical',
          'allowTyping': false, //User gets a text box to type into
          'allowMultiple': false,   /// Lets you select dorp-down options one at a time, can click multiple at a time - Useful but not for here
          'allowNone' : false //disables the "Select a value" - it's confusing
        }
      },
      state: {
        selectedValues: ['Absolute']
      }
    });
  
    //Second Control wrapper  - Sliding bar that Filters by Year of Data
    var TypePicker = new google.visualization.ControlWrapper({
      'controlType': 'NumberRangeFilter',
      'containerId': 'filter2_div',
      'options': {
        'filterColumnLabel': 'Years',
        'ui': {
          'label': 'Select Year Range',
          format: {pattern: '0000'},
          'labelStacking': 'vertical',
          'allowTyping': false, 
          'allowMultiple': false  
        }
      }
    });
    
    //Actual chart wrapper here
    var DashColumnChart = new google.visualization.ChartWrapper({
      'chartType': 'ColumnChart',
      'containerId': 'health_dashboard_div',
      view: {columns: [1,2,3,4,5,6,7,8,9,10,11]},
      options : {
                      chartArea: {width:'60%', height:'60%'},
                      width : 1000,
                      height: 400,
                      annotations: {alwaysOutside: true},
                      vAxis: {title: 'Spending',  format: 'short', },
                      hAxis: {title: 'Year', slantedText: false, format:'#,####'},
                      tooltip: {format:'scientific'},    
                      //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                      colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',]             
                  }
  
    });
  
    //Bind the control wrapers to the data, then draw the chart
    var dashboard = new google.visualization.Dashboard(document.getElementById('health_dashboard_div')).
      bind([namePicker, TypePicker], DashColumnChart).
      draw(data)
  
  } // End of the dashboard script




  
function drawDashboard_health_mil(response) {
    var data = response.getDataTable();
    console.log(data)
   
    //First Control wrapper  - Filters by Category of Data
    var namePicker = new google.visualization.ControlWrapper({
      'controlType': 'CategoryFilter',
      'containerId': 'filter_mil_div',
      'options': {
        'filterColumnLabel': 'Country',
        'ui': {
          'label': 'Add Countries to Viewer',
          'labelStacking': 'vertical',
          'allowTyping': false, //User gets a text box to type into
          'allowMultiple': true,   /// Lets you select drop-down options one at a time, can click multiple at a time - Useful but not for here
          'allowNone' : false //disables the "Select a value" - it's confusing
        }
      },
      state: {
        selectedValues: ['United States', 'China']
      }
    });
  
    //Second Control wrapper  - Sliding bar that Filters by Year of Data
    var TypePicker = new google.visualization.ControlWrapper({
      'controlType': 'NumberRangeFilter',
      'containerId': 'filter2_mil_div',
      'options': {
        'filterColumnLabel': 'Years',
        'ui': {
          'label': 'Select Year Range',
          format: {pattern: '0000'},
          'labelStacking': 'vertical',
          'allowTyping': false, 
          'allowMultiple': false  
        }
      }
    });
    
    //Actual chart wrapper here
    var DashColumnChart = new google.visualization.ChartWrapper({
      'chartType': 'ColumnChart',
      'containerId': 'health_mil_dashboard_div',
      view: {columns: [0,3,4]},
      options : {
                      chartArea: {width:'80%', height:'50%'},
                      width : 1200,
                      height: 600,
                      isStacked: true,
                      annotations: {alwaysOutside: true},
                      vAxis: {title: 'Spending',  format: 'short', },
                      hAxis: {title: 'Year', slantedText: true, textStyle: {fontSize: 14}},
                      tooltip: {format:'scientific'},    
                      //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                      colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',]             
                  }
  
    });
  
    //Bind the control wrapers to the data, then draw the chart
    var dashboard = new google.visualization.Dashboard(document.getElementById('health_mil_dashboard_div')).
      bind([namePicker, TypePicker], DashColumnChart).
      draw(data)
  
  } // End of the dashboard script drawDashboard_health_mil



  function drawDashboard_health_bubble_gdp(response) {
    var data = response.getDataTable();
  
  
      //First Control wrapper  - Filters by Category of Data
      var namePicker = new google.visualization.ControlWrapper({
      'controlType': 'CategoryFilter',
      'containerId': 'filter_gdp_div',
      'options': {
        'filterColumnLabel': 'Country',
        'ui': {
          'label': 'Select countries to Display',
          'labelStacking': 'vertical',
          'allowTyping': false, //User gets a text box to type into
          'allowMultiple': true,   /// Lets you select dorp-down options one at a time, can click multiple at a time - Useful but not for here
          'allowNone' : false //disables the "Select a value" - it's confusing
        }
      },
      state: {
        selectedValues: ['United States', 'Germany', 'Australia', 'France', 'Japan',
                      'United Kingdom', 'Italy', 'South Korea', 'Brazil', 'China']
      }
    });
  
    //Second Control wrapper  - Sliding bar that Filters by Year of Data
    var TypePicker = new google.visualization.ControlWrapper({
      'controlType': 'NumberRangeFilter',
      'containerId': 'filter2_gdp_div',
      'options': {
        'filterColumnLabel': 'Year',
        'ui': {
          'label': 'Select Year Range',
          format: {pattern: '0000'},
          'labelStacking': 'vertical',
          'allowTyping': false, 
          'allowMultiple': false  
        }
      }
    });
  
  
  //Need to calculate the range to adjust the frame to the bubblesize or will cut off. Not done automatically for some reason.
    var rangeX = data.getColumnRange(1);
    var fractionX = (rangeX.max -rangeX.min)*0.1;
  
    var rangeY = data.getColumnRange(2);
    var fractionY = (rangeY.max -rangeY.min)*0.2;
  
    var DashColumnChart = new google.visualization.ChartWrapper({
      'chartType': 'BubbleChart',
      'containerId': 'health_gdp_dashboard_div',
      view: {columns: [0,1,2,3]},
      options : {
                      chartArea: {width:'60%', height:'60%'},
                      width : 1000,
                      height: 400,
                      sizeAxis :{ maxSize: 20},
                      vAxis: {title: 'Spending',
                              viewWindow: { 
                                  min: rangeY.min-fractionY,
                                  max: rangeY.max+fractionY
                                  },
                              format: 'short',  },
                      hAxis: {title: 'Per Capita Healthcare Spending',  
                              viewWindow: { 
                                  min: rangeX.min-fractionX,
                                  max: rangeX.max+fractionX
                                  },
                              format: 'short',  },
                      //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                      colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',]             
                  }
  
    });
  
  
        var dashboard = new google.visualization.Dashboard(document.getElementById('health_gdp_dashboard_div')).
      bind([namePicker, TypePicker], DashColumnChart).
      draw(data)
  
      }//End BubbleChart




      function drawLineHealthDashboard(response) {
        var data = response.getDataTable();
       
        //First Control wrapper  - Filters by Category of Data
        var namePicker = new google.visualization.ControlWrapper({
          'controlType': 'CategoryFilter',
          'containerId': 'filter_health_change_div',
          'options': {
            'filterColumnLabel': 'Type',
            'ui': {
              'label': 'Spending Representation',
              'labelStacking': 'vertical',
              'allowTyping': false, //User gets a text box to type into
              'allowMultiple': false,   /// Lets you select dorp-down options one at a time, can click multiple at a time - Useful but not for here
              'allowNone' : false //disables the "Select a value" - it's confusing
            }
          },
          state: {
            selectedValues: ['Absolute']
          }
        });
      
        
        //Actual chart wrapper here
        var DashColumnChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'health_change_dashboard_div',
          view: {columns: [1,2,3,4,5,6,7,8,9,10,11]},
          options : {
                          chartArea: {width:'60%', height:'60%'},
                          width : 1000,
                          height: 400,
                          vAxis: {title: 'Spending',  format: 'short', gridlines: {color: 'transparent'}},
                          hAxis: {title: 'Year', slantedText: false, format:'#,####', minorGridlines: {color: 'transparent'} },
                          //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                          colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',],   
                          explorer: { 
                  actions: ['dragToZoom', 'rightClickToReset'],
                  keepInBounds: true,
                  maxZoomIn: 4.0},          
                      },
                  
      
        });
      
        //Bind the control wrapers to the data, then draw the chart
        var dashboard = new google.visualization.Dashboard(document.getElementById('health_change_dashboard_div')).
          bind([namePicker], DashColumnChart).
          draw(data)
      

} // End of the dashboard script  - Line Plot 

var geo_mode = "Percent";
function changeView() {

    if(geo_mode == "Absolute"){
      drawSheetName ('Global_HEAL', 'SELECT A,B,D', drawGeoDashboard);
    geo_mode = "Percent"
  }else{
    drawSheetName ('Global_HEAL', 'SELECT A,B,C', drawGeoDashboard);
    geo_mode = "Absolute"
  }
};

function drawGeoDashboard(response) {
  var data = response.getDataTable();
  console.log(data)
 

  //Control wrapper  -  Filters by Year of Data
  var TypePicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'filter_health_geo_div',
    'options': {
      'filterColumnLabel': 'Years',
      'ui': {
        'label': 'Select Year Range',
        'labelStacking': 'vertical',
        'allowTyping': false, 
        'allowMultiple': false,
        'allowNone' : false  
      }
    },
    state: {
      selectedValues: ['2011-2017']}
  });
  
  
  //Get range so the gradient range is consistant
  var lim_value;
  var range = data.getColumnRange(2);
  lim_value = (range.max-range.min);


  //Actual chart wrapper here
  var DashColumnChart = new google.visualization.ChartWrapper({
    'chartType': 'GeoChart',
    'containerId': 'health_geo_dashboard_div',
    view: {columns: [0,2]},
    options : {
                    chartArea: {width:'70%', height:'70%'},
                    width : 1000,
                    height: 500,
                    colorAxis: {minValue:range.min, maxValue:range.max, colors: ['blue','green','yellow','orange',]},
                    backgroundColor: {fill:"#E0e2e3", },
                    legend: {textStyle: {fontSize: 14}},

                          
                }

  });

  //Bind the control wrapers to the data, then draw the chart
  var dashboard = new google.visualization.Dashboard(document.getElementById('health_geo_dashboard_div')).
    bind([TypePicker], DashColumnChart).
    draw(data)

} // End of the Geochart dashboard script




///Start of Education Plots



function drawDashboard_edu(response) {
  var data = response.getDataTable();
  

  console.log(data)
 
  //First Control wrapper  - Filters by Category of Data
  var namePicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'filter_edu_div',
    'options': {
      'filterColumnLabel': 'Type',
      'ui': {
        'label': 'Spending Representation',
        'labelStacking': 'vertical',
        'allowTyping': false, //User gets a text box to type into
        'allowMultiple': false,   /// Lets you select dorp-down options one at a time, can click multiple at a time - Useful but not for here
        'allowNone' : false //disables the "Select a value" - it's confusing
      }
    },
    state: {
      selectedValues: ['Absolute']
    }
  });

  //Second Control wrapper  - Sliding bar that Filters by Year of Data
  var TypePicker = new google.visualization.ControlWrapper({
    'controlType': 'NumberRangeFilter',
    'containerId': 'filter2_edu_div',
    'options': {
      'filterColumnLabel': 'Years',
      'ui': {
        'label': 'Select Year Range',
        format: {pattern: '0000'},
        'labelStacking': 'vertical',
        'allowTyping': false, 
        'allowMultiple': false  
      }
    }
  });
  
  //Actual chart wrapper here
  var DashColumnChart = new google.visualization.ChartWrapper({
    'chartType': 'ColumnChart',
    'containerId': 'edu_dashboard_div',
    view: {columns: [1,2,3,4,5,6,7,8,9,10,11]},
    options : {
                    chartArea: {width:'60%', height:'60%'},
                    width : 1000,
                    height: 400,
                    annotations: {alwaysOutside: true},
                    vAxis: {title: 'Spending',  format: 'short', },
                    hAxis: {title: 'Year', slantedText: false, format:'#,####'},
                    tooltip: {format:'scientific'},    
                    //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                    colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',]             
                }

  });

  //Bind the control wrapers to the data, then draw the chart
  var dashboard = new google.visualization.Dashboard(document.getElementById('edu_dashboard_div')).
    bind([namePicker, TypePicker], DashColumnChart).
    draw(data)

} // End of the dashboard script





function drawDashboard_edu_mil(response) {
  var data = response.getDataTable();
  console.log(data)
 
  //First Control wrapper  - Filters by Category of Data
  var namePicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'filter_edu_mil_div',
    'options': {
      'filterColumnLabel': 'Country',
      'ui': {
        'label': 'Add Countries to Viewer',
        'labelStacking': 'vertical',
        'allowTyping': false, //User gets a text box to type into
        'allowMultiple': true,   /// Lets you select drop-down options one at a time, can click multiple at a time - Useful but not for here
        'allowNone' : false //disables the "Select a value" - it's confusing
      }
    },
    state: {
      selectedValues: ['United States',]
    }
  });

  //Second Control wrapper  - Sliding bar that Filters by Year of Data
  var TypePicker = new google.visualization.ControlWrapper({
    'controlType': 'NumberRangeFilter',
    'containerId': 'filter2_edu_mil_div',
    'options': {
      'filterColumnLabel': 'Years',
      'ui': {
        'label': 'Select Year Range',
        format: {pattern: '0000'},
        'labelStacking': 'vertical',
        'allowTyping': false, 
        'allowMultiple': false  
      }
    }
  });
  
  //Actual chart wrapper here
  var DashColumnChart = new google.visualization.ChartWrapper({
    'chartType': 'ColumnChart',
    'containerId': 'edu_mil_dashboard_div',
    view: {columns: [0,3,4]},
    options : {
                    chartArea: {width:'80%', height:'50%'},
                    width : 1200,
                    height: 600,
                    isStacked: true,
                    annotations: {alwaysOutside: true},
                    vAxis: {title: 'Spending',  format: 'short', },
                    hAxis: {title: 'Year', slantedText: true, textStyle: {fontSize: 14}},
                    tooltip: {format:'scientific'},    
                    //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                    colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',]             
                }

  });

  //Bind the control wrapers to the data, then draw the chart
  var dashboard = new google.visualization.Dashboard(document.getElementById('edu_mil_dashboard_div')).
    bind([namePicker, TypePicker], DashColumnChart).
    draw(data)

} // End of the dashboard script drawDashboard_health_mil



function drawDashboard_edu_bubble_gdp(response) {
  var data = response.getDataTable();


    //First Control wrapper  - Filters by Category of Data
    var namePicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'filter_edu_gdp_div',
    'options': {
      'filterColumnLabel': 'Country',
      'ui': {
        'label': 'Select countries to Display',
        'labelStacking': 'vertical',
        'allowTyping': false, //User gets a text box to type into
        'allowMultiple': true,   /// Lets you select dorp-down options one at a time, can click multiple at a time - Useful but not for here
        'allowNone' : false //disables the "Select a value" - it's confusing
      }
    },
    state: {
      selectedValues: ['United States', ]
    }
  });

  //Second Control wrapper  - Sliding bar that Filters by Year of Data
  var TypePicker = new google.visualization.ControlWrapper({
    'controlType': 'NumberRangeFilter',
    'containerId': 'filter2_edu_gdp_div',
    'options': {
      'filterColumnLabel': 'Year',
      'ui': {
        'label': 'Select Year Range',
        format: {pattern: '0000'},
        'labelStacking': 'vertical',
        'allowTyping': false, 
        'allowMultiple': false  
      }
    }
  });


//Need to calculate the range to adjust the frame to the bubblesize or will cut off. Not done automatically for some reason.
  var rangeX = data.getColumnRange(1);
  var fractionX = (rangeX.max -rangeX.min)*0.1;

  var rangeY = data.getColumnRange(2);
  var fractionY = (rangeY.max -rangeY.min)*0.2;

  var DashColumnChart = new google.visualization.ChartWrapper({
    'chartType': 'BubbleChart',
    'containerId': 'edu_gdp_dashboard_div',
    view: {columns: [0,1,2,3]},
    options : {
                    chartArea: {width:'60%', height:'60%'},
                    width : 1000,
                    height: 400,
                    sizeAxis :{ maxSize: 20},
                    vAxis: {title: 'Spending',
                            viewWindow: { 
                                min: rangeY.min-fractionY,
                                max: rangeY.max+fractionY
                                },
                            format: 'short',  },
                    hAxis: {title: 'Per Capita Healthcare Spending',  
                            viewWindow: { 
                                min: rangeX.min-fractionX,
                                max: rangeX.max+fractionX
                                },
                            format: 'short',  },
                    //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                    colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',]             
                }

  });


      var dashboard = new google.visualization.Dashboard(document.getElementById('edu_gdp_dashboard_div')).
    bind([namePicker, TypePicker], DashColumnChart).
    draw(data)

    }//End BubbleChart




    function drawLineEduDashboard(response) {
      var data = response.getDataTable();
     
      //First Control wrapper  - Filters by Category of Data
      var namePicker = new google.visualization.ControlWrapper({
        'controlType': 'CategoryFilter',
        'containerId': 'filter_edu_change_div',
        'options': {
          'filterColumnLabel': 'Type',
          'ui': {
            'label': 'Spending Representation',
            'labelStacking': 'vertical',
            'allowTyping': false, //User gets a text box to type into
            'allowMultiple': false,   /// Lets you select dorp-down options one at a time, can click multiple at a time - Useful but not for here
            'allowNone' : false //disables the "Select a value" - it's confusing
          }
        },
        state: {
          selectedValues: ['Absolute']
        }
      });
    
      
      //Actual chart wrapper here
      var DashColumnChart = new google.visualization.ChartWrapper({
        'chartType': 'LineChart',
        'containerId': 'edu_change_dashboard_div',
        view: {columns: [1,2,3,4,5,6,7,8,9,10,11]},
        options : {
                        chartArea: {width:'60%', height:'60%'},
                        width : 1000,
                        height: 400,
                        vAxis: {title: 'Spending',  format: 'short', gridlines: {color: 'transparent'}},
                        hAxis: {title: 'Year', slantedText: false, format:'#,####', minorGridlines: {color: 'transparent'} },
                        //colors: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#000',]  
                        colors: ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#bfef45', '#000',],   
                        explorer: { 
                actions: ['dragToZoom', 'rightClickToReset'],
                keepInBounds: true,
                maxZoomIn: 4.0},          
                    },
                
    
      });
    
      //Bind the control wrapers to the data, then draw the chart
      var dashboard = new google.visualization.Dashboard(document.getElementById('edu_change_dashboard_div')).
        bind([namePicker], DashColumnChart).
        draw(data)
    

} // End of the dashboard script  - Line Plot 

var geo_mode_edu = "Percent";
function changeView_edu() {

  if(geo_mode_edu == "Absolute"){
    drawSheetName ('Global_EDU', 'SELECT A,B,D', drawGeoDashboardEdu);
    geo_mode_edu = "Percent"
}else{
  drawSheetName ('Global_EDU', 'SELECT A,B,C', drawGeoDashboardEdu);
  geo_mode_edu = "Absolute"
}
};

function drawGeoDashboardEdu(response) {
var data = response.getDataTable();
console.log(data)


//Control wrapper  -  Filters by Year of Data
var TypePicker = new google.visualization.ControlWrapper({
  'controlType': 'CategoryFilter',
  'containerId': 'filter_edu_geo_div',
  'options': {
    'filterColumnLabel': 'Years',
    'ui': {
      'label': 'Select Year Range',
      'labelStacking': 'vertical',
      'allowTyping': false, 
      'allowMultiple': false,
      'allowNone' : false  
    }
  },
  state: {
    selectedValues: ['2011-2017']}
});


//Get range so the gradient range is consistant
var lim_value;
var range = data.getColumnRange(2);
lim_value = (range.max-range.min);


//Actual chart wrapper here
var DashColumnChart = new google.visualization.ChartWrapper({
  'chartType': 'GeoChart',
  'containerId': 'edu_geo_dashboard_div',
  view: {columns: [0,2]},
  options : {
                  chartArea: {width:'70%', height:'70%'},
                  width : 1000,
                  height: 500,
                  colorAxis: {minValue:range.min, maxValue:range.max, colors: ['blue','green','yellow','orange',]},
                  backgroundColor: {fill:"#E0e2e3", },
                  legend: {NumberFormat: "scientific",  textStyle: {fontSize: 14}},

                        
              }

});

//Bind the control wrapers to the data, then draw the chart
var dashboard = new google.visualization.Dashboard(document.getElementById('edu_geo_dashboard_div')).
  bind([TypePicker], DashColumnChart).
  draw(data)

} // End of the Geochart dashboard script