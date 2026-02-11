window.onload = function () {
    populateMunicipalities();
  };
  
  var municipalities = [
  'Stockholm',
  'Jönköping',
  'Linköping',
  'Göteborg',
  'Norrköping',
  'Malm',
  'Ängelholm',
  'Norrtälj',
  'Nack',
  'Enköping',
  'Liding',
  'Helsingborg',
  'Gävl',
  'Danderyd',
  'Lund',
  'Sundbyberg',
  'Sollentun',
  'Järfäll',
  'Mölndal',
  'Uddevall',
  'Uppsal',
  'Bromöll',
  'Salem',
  'Täb',
  'Borläng',
  'Hudding',
  'Österåker',
  'Västerå',
  'Härnösand',
  'Växj',
  'Soln',
  'Skövd',
  'Karlstad',
  'Borå',
  'Kungsback',
  'Mor',
  'Borgholm',
  'Oskarshamn',
  'Klippan',
  'Trollhättan',
  'Örebr',
  'Svedal',
  'Avest',
  'Lysekil',
  'Falkenberg',
  'Vårgård',
  'Karlsborg',
  'Karlskron',
  'Nässj',
  'Varberg',
  'Vimmerb',
  'Ystad',
  'Kungälv',
  'Kil',
  'Skellefte',
  'Västervik',
  'Sigtun',
  'Trelleborg',
  'Haning',
  'Höganä',
  'Sandviken',
  'Östhammar',
  'Sundsvall',
  'Landskron',
  'Södertälj',
  'Lerum',
  'Sal',
  'Tyres',
  'Staffanstorp',
  'Värmd',
  'Vänersborg',
  'Båstad',
  'Eskilstun',
  'Ume',
  'Hab',
  'Kalma',
  'Lule',
  'Vallentun',
  'Partill',
  'Tros',
  'Arvik',
  'Haparand',
  'Botkyrk',
  'Svalöv',
  'Lomm',
  'UpplandsVäsb',
  'Hammar',
  'Timr',
  'Säffl',
  'Katrineholm',
  'Mark',
  'Skar',
  'Gotland',
  'Östersund',
  'Arbog',
  'Fal',
  'Halmstad',
  'Upplands-Bro',
  'Al',
  'Rättvik',
  'Velling',
  'Gällivar',
  'Perstorp',
  'Ulricehamn',
  'Skurup',
  'Alingså',
  'Nyköping',
  'Karlshamn',
  'Värnam',
  'Leksand',
  'Kristianstad',
  'Vaxholm',
  'Oxelösund',
  'Burlöv',
  'Karlskog',
  'Söderhamn',
  'Motal',
  'Mjölb',
  'Kirun',
  'Örnsköldsvik',
  'Sjöb',
  'Ludvik',
  'Hudiksvall',
  'Boden',
  'Hofor',
  'Mariestad',
  'Lidköping',
  'Bjuv',
  'ÖstraGöing',
  'Ronneb',
  'Kungsör',
  'Falköping',
  'Finspång',
  'Essung',
  'Strömstad',
  'LillaEdet',
  'Kristinehamn',
  'Orus',
  'Stenungsund',
  'Strängnä',
  'Heb',
  'År',
  'Tidaholm',
  'Hässleholm',
  'Härjedalen',
  'Åstorp',
  'Tomelill',
  'Eslöv',
  'Valdemarsvik',
  'Osb',
  'Grästorp',
  'Olofström',
  'Hallstahammar',
  'Kramfor',
  'Smedjebacken',
  'Ång',
  'Pite',
  'Öcker',
  'Älvkarleb',
  'Färgeland',
  'Alvest',
  'Vännä',
  'Laholm',
  'Tierp',
  'Hallsberg',
  'Nor',
  'Vetland',
  'Lindesberg',
  'Mörbylång',
  'Hj',
  'Kävling',
  'Sunn',
  'Ljusdal',
  'Forshag',
  'Uppviding',
  'Tibr',
  'Lekeberg',
  'Tjörn',
  'Herrljung',
  'Härryd',
  'Lesseb',
  'Boxholm',
  'Bollnä',
  'Älmhult',
  'Åtvidaberg',
  'Tranem',
  'Hylt',
  'Ockelb',
  'Tranå',
  'Ljungb',
  'Törebod',
  'Övertorne',
  'Hedemor',
  'Nynäshamn',
  'Hällefor',
  'Simrishamn',
  'Fagerst',
  'Hagfor',
  'Gagnef',
  'Torsb',
  'Surahammar',
  'Torså',
  'Nykvarn',
  'Filipstad',
  'Sölvesborg',
  'Kali',
  'Tingsryd',
  'Nybr',
  'Eker',
  'Vaggeryd',
  'Askersund',
  'Höör',
  'Söderköping',
  'Strömsund',
  'Knivst',
  'Emmabod',
  'Årjäng',
  'Var',
  'Vingåker',
  'S',
  'Örkelljung',
  'Bengtsfor',
  'Mönsterå',
  'Skinnskatteberg',
  'Gnosj',
  'Tanum',
  'Vadsten',
  'Nordanstig',
  'Grum',
  'Gislaved',
  'C',
  'Hörb',
  'Tre',
  'Köping',
  'Eksj',
  'Flen',
  'Krokom',
  'Håb',
  'Robertsfor',
  'Sollefte',
  'Hultsfred',
  'Älvdalen',
  'Åmål',
  'Lycksel'];
  
  function populateMunicipalities() {
    var select = document.getElementById("municipalities");
    municipalities.forEach(function (municipality) {
      var option = document.createElement("option");
      option.value = municipality;
      option.textContent = municipality;
      select.appendChild(option);
    });
  }

  
  function prediction() {
    document.getElementById("pred_value").textContent = "Predicting...";
    var municipalityInput = document.getElementById("municipalities").value.trim();
  
    var municipalityError = document.getElementById("municipalityError");
    municipalityError.textContent = "";
  
    if (!municipalities.includes(municipalityInput)) {
      municipalityError.textContent =
        "Please select a valid Municipality from the list.";
      return;
    }
  
    // Validate Living Area
    var livingAreaInput = parseFloat(
      document.getElementById("living_area").value
    );
    var livingAreaError = document.getElementById("livingAreaError");
    livingAreaError.textContent = "";
  
    if (isNaN(livingAreaInput) || livingAreaInput <= 0) {
      livingAreaError.textContent =
        "Living Area must be a positive number greater than 0.";
      return;
    }

    let xmlr = new XMLHttpRequest();
    xmlr.open("POST", "/predict", true);
  
    xmlr.setRequestHeader("Content-Type", "application/json;charset = utf-8");
  
    xmlr.onreadystatechange = function () {
      if (xmlr.readyState == 4) {
        if (xmlr.status == 200) {
          let jsonResponse = JSON.parse(xmlr.responseText);
          document.getElementById("pred_value").textContent =
            jsonResponse.value + " million in Kr";
          console.log("Success");
        } else {
          console.error("Error");
        }
      }
    };
  
    var formData = {
      House_type: document.getElementById("houseType").value,
      Municipality: document.getElementById("municipalities").value,
      Living_area: document.getElementById("living_area").value,
      Built_On: document.getElementById("built_on").value,
      Lift: document.getElementById("lift").value,
      Balcony: document.getElementById("balcony").value,
    };
  
    xmlr.send(JSON.stringify(formData));
  }
  