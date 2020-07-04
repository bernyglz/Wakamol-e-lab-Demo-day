// Scatter Plot
d3.json('/datos').then(function(data){

  //console.log(data[0]);
  //console.log(data[0].name);
  //console.log(data.length);
  
    var name = [];
    var propiedad = [];
    var entidad = [];
    var price = [];
    var rooms = [];
    var bathrooms = [];
    var construction = [];
    var terrain = [];
    var lat = [];
    var lng = [];
    var colonia = [];
    var monto = [];

    // For each row
    for (var index = 0; index < data.length; index++) {
      // Add to the arrays
      name.push(data[index].name);
      propiedad.push(data[index].propiedad);
      entidad.push(data[index].entidad);
      price.push(data[index].price);
      rooms.push(data[index].rooms);
      bathrooms.push(data[index].bathrooms);
      construction.push(data[index].construction);
      terrain.push(data[index].terrain);
      lat.push(data[index].lat);
      lng.push(data[index].lng);
      colonia.push(data[index].colonia);
      monto.push(data[index].Monto1);
    }
    
    // Scatter Plot Longitud y Latitud:
    var precio_m2 = [];
      for (var i = 0; i < monto.length; i++ ){
        precio_m2.push( new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' } ).format( Math.round(monto[i] / construction[i] ) ) );
      };

    var texto = [];
      for (var i = 0; i < precio_m2.length; i++ ){
        texto.push( 'MXN ' + precio_m2[i] + '/m2 de construcción, con ' 
        + rooms[i] + ' cuartos, ' 
        + bathrooms[i] + ' baños y ' 
        + construction[i] + ' m2 en ' 
        + colonia[i] + ', ' + entidad[i]);
      };

    var trace1 = {
      y: lat,
      x: lng,
      text: texto,
      mode: 'markers',
      type: 'scatter',
      hoverinfo: 'text',
      marker: { size: monto/1000000,  color: monto }
    };

    var layout = {
      title:'How is the housing offer distributed in the metropolitan area of Mexico City? <br /> (Price per m2)',
      yaxis: { title: 'Latitud'},
      xaxis: { title: 'Longitud'},
    };
    
    var data = [trace1];

    Plotly.newPlot('Scatter-Plot', data, layout);

  // Scatter Plot Precio y Construcción (m2):
  //var texto2 = [];
  //    for (var i = 0; i < price.length; i++ ){
  //      texto.push(price[i] + ', ' 
  //      + construction[i] + ' m2');
  //    }

  //var trace1 = {
  //  y: monto,
  //  x: construction,
  //  text: texto2,
  //  mode: 'markers',
  //  type: 'scatter',
  //  hoverinfo: 'text'
  //};

  //var layout = {
  //  title:'¿Cómo se relaciona el precio del inmueble con los m2 de construcción?',
  //  yaxis: { title: 'Precio en MXN'},
  //  xaxis: { title: 'Construccion en m2'},
  //};
  
  //var data = [trace1];

  //Plotly.newPlot('Scatter-Construction', data, layout);

   });


