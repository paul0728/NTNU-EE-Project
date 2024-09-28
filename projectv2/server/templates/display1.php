<?php

$db = new SQLite3('test.db');
$res = $db->query('SELECT * FROM projects where name=species');

while ($row = $res->fetchArray()) {
    echo "{$row['id']} {$row['name']} {$row['price']} \n";
}

?>

<!DOCTYPE html>
<head>
<meta charset="UTF-8" />
<title>魚類辨識、偵測長度系統</title>
</head>

<body>
<form action=""method="POST" >
  <label for="species">魚種</label>
  <input type="text"id=species name="species"list="species_">
  <datalist id="species_">
    <option value="Cantherhines_dumerilii"></option>
    <option value="Caranx_melampygus"></option>
    <option value="Cephalopholis_leopardus"></option>
    <option value="Cirrhilabrus_cyanopleura"></option>
    <option value="Epinephelus_quoyanus"></option>
    <option value="Hemigymnus_fasciatus"></option>
    <option value="Leptojulis_cyanopleura"></option>
    <option value="Pseudanthias_squamipinnis"></option>
    <option value="Thalassoma_lunare"></option>
  </datalist>
</form>
<label for="length">魚長(公尺)</label>
<input type="text"id=length name="length"list="length_">
<datalist id="length_">
    <option value="0-1"></option>
    <option value="1-1.5"></option>
    <option value="1.5-2"></option>
    <option value="2-2.5"></option>
    <option value="2.5-3"></option>
    <option value=">3"></option>
</datalist>
<input type=submit value="檢索">

</form>


<table width="700" border="1">
  <thead>
    <tr>
      <th>id</th>
      <th>name</th>
      <th>species</th>
    <tr>

    <tr>
{% for row in value %} 
    <tr>
        <td>{{row[0]}}</td>
        <td>{{row[1]}}</td>
        <td>{{row[2]}}</td>
    </tr>
        {% endfor %}
</table>


</body>
</html>


