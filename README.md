festescat
=========

festes.cat
<html>
<body>
<h1>FESTES.CAT</h1>

Aplicacio desenvolupada per Eduard Renye i Victor Diaz

FESTES - EVENTS - UBICACIONS - USUARIS
-----------------------------------------------------------
Tota aquesta informacio esta disponible ens els formats: JSON,HTML i XML 

<table>
	<tr>
	  <td><strong>Method</strong></td>
	  <td><strong>Resources</strong></td>
	  <td><strong>Description</strong></td>
	</tr>
	
	<tr>
	  <td>GET</td>
	  <td>/api/festes</td>
	  <td>Totes les festes disponibles</td>
	</tr>

	<tr>
	  <td>POST</td>
	  <td>/api/festes</td>
	  <td>Afegir una festa</td>
	</tr>

	<tr>
	  <td>GET</td>
	  <td>/api/festes/ID</td>
	  <td>Informacio d'una festa en concret</td>
	</tr>

	<tr>
	  <td>PUT</td>
	  <td>/api/festes/ID</td>
	  <td>Afegir o modificar una festa</td>
	</tr>

	<tr>
	  <td>DELETE</td>
	  <td>/api/festes/ID</td>
	  <td>Elimina una festa</td>
	</tr>

	<tr>
	  <td>GET</td>
	  <td>/api/events</td>
	  <td>Tots els events disponibles</td>
	</tr>

	<tr>
	  <td>POST</td>
	  <td>/api/events</td>
	  <td>Afegir un event</td>
	</tr>

	<tr>
	  <td>GET</td>
	  <td>/api/events/ID</td>
	  <td>Informacio d'un event</td>
	</tr>

	<tr>
	  <td>PUT</td>
	  <td>/api/events/ID</td>
	  <td>Afegir o modificar un event</td>
	</tr>

	<tr>
	  <td>DELETE</td>
	  <td>/api/events/ID</td>
	  <td>Elimina un event</td>
	</tr>

	<tr>
	  <td>GET</td>
	  <td>/api/ubicacions</td>
	  <td>Totes les ubicacions disponibles</td>
	</tr>

	<tr>
	  <td>POST</td>
	  <td>/api/ubicacions</td>
	  <td>Afegir una ubicacio</td>
	</tr>

	<tr>
	  <td>GET</td>
	  <td>/api/ubicacions/ID</td>
	  <td>Informacio de una ubicacio</td>
	</tr>

	<tr>
	  <td>PUT</td>
	  <td>/api/ubicacions/ID</td>
	  <td>Afegir o modificar una ubicacio</td>
	</tr>

	<tr>
	  <td>DELETE</td>
	  <td>/api/ubicacions/ID</td>
	  <td>Elimina una ubicacio</td>
	</tr>

</table>
Maquetació feta amb bootstrap (CSS i JS).

Semantica:
	Entitat Festes: Hem usat el tipus EntertainmentBusiness que conté reviews i està relacionat amb events.
	Entitat Events: Hem usat el tipus event i està relacionat amb ubicacions.
	Entitat Ubicacions: Hem usat el tipus Place.
</body>
</html>
