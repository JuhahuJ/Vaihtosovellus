# Vaihtosovellus

## Lopullinen tilanne

Sovelluksessa voi luoda tavallisen käyttäjän, tai adminkäyttäjän. 

Tavallinen käyttäjä voi luoda alueita ja pyyntöjä alueille ja muokata luomiaan pyyntöjä.

Adminkäyttäjä voi tehdä samat asiat, kuin tavallinen käyttäjä + poistaa alueita, vaihtaa yleisen admin salasanan, resetoida yleisen admin salasanan, muokata kaikkia pyyntöjä ja nähdä listan käyttäjistä, jotka eivät ole adminkäytäjiä, ja poistaa niitä.

Sovellukseen on luotu yksi alkuperäinen adminkäyttäjä, jonka nimi on admin ja salasana on 1234.

Yleinen admin salasana, jonka avulla voi luoda uusia admin käyttäjiä, on abc123, jos sitä ei ole muutettu.

Sovellusta voi testata herokussa osoitteessa https://vaihtosovellus.herokuapp.com/

## Tavoite

Sovellus, jonka avulla käyttäjät voivat julkaista vaihtopyyntöjä, joiden avulla voi vaihtaa esineitä ja muita asioita.
Esimerkiksi käyttäjä 1 pyytää pyörän pumppua ja tarjoaa vaihdossa pumpun antajan kanssa sovittavaa palvelua, esim. nurmikon leikkaus.
Jokainen käyttäjä on joko peruskäyttäjä tai ylläpitäjä.

-käyttäjä voi kirjautua sisään

-käyttäjä näkee listan alueista, joissa on vaihtopyyntöjä

-käyttäjä voi luoda alueita

-käyttäjä voi lisätä alueelle vaihtopyynnön, muokata sitä tai poistaa sen

-vaihtopyyntöön voi lisätä mitä haluaa, mitä tarjoaa, yhteystietoja

-ylläpitäjä voi lisätä ja poistaa alueita
