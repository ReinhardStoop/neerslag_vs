# **Evaluatie Exreme neerslag**

# 0. Probleemstelling extreme neerslag

Noot: repliceerbaarheid en versioning:

Indien deze nota in pdf of Word beschikbaar is, kan men steeds de nieuwste versie en de repliceerbare code op GitHub vinden:
https://github.com/ReinhardStoop/neerslag_vs

## 0.1. Context

Op de website van Statistiek Vlaanderen wordt een VOS gepubliceert over neerslagextremen.
Zie https://www.vlaanderen.be/statistiek-vlaanderen/milieu-en-natuur/neerslagextremen

Deze cijfers en trendanalyse worden aangeleverd door VMM, die deze ook zelf online publiceert.
Zie https://vmm.vlaanderen.be/feiten-cijfers/klimaat/klimaatthemas/wateroverlast-door-hevige-regenval/indicator-neerslagextremen

Ook het KMI publiceert deze gegevens en analyse:
https://www.meteo.be/nl/klimaat/klimaatverandering-in-belgie/klimaattrends-in-ukkel/neerslag/extremiteitsindices/max-10-dagen-neerslag

Op de website van het KMI vindt men ook klimaatrapporten waarin de methodologie voor trendanalyses op klimaattijdreeksen wordt uitgelegd.
Zie https://www.meteo.be/nl/klimaat/klimaatverandering-in-belgie/klimaatrapporten

Het klimaatrapport van 2020 geeft helder weer welke methodologische overwegingen belangrijk zijn bij het analyseren van klimaattijdreeksen. 

We gebruiken in deze kwaliteitsevaluatie ook expliciet het volgende referentiewerk van KNMI, dat aansluit bij de KMI-klimaatrapportering:
KNMI: **Standard method for determining a climatological trend**, C.F. de Valk, De Bilt, 2020, Technical report TR-389.
https://cdn.knmi.nl/system/ckeditor_assets/attachments/161/TR389.pdf

## 0.2. Vaststelling

Heel algemeen wijken de trendberekeningen en voorstellingen van VMM soms af van die van het KMI.

In het bijzonder bekijken we in deze nota de reeks van neerslagextremen over 10 dagen. Door VMM (en overgenomen door VSA) wordt op de volledige tijdreeks een regressieanalyse toegepast, met als conclusie dat er een *positieve significante* trend is. Op de website van het KMI echter wordt deze reeks visueel voorgesteld op basis van LOESS (zie verder) en wordt een recente trendberekening (30 jaar) apart beoordeeld, deze is dan *niet significant*.


## 0.3. Doelstelling

We doen een replicatie en evaluatie van deze berekeningen. De analyse wordt uitgevoerd in Python op een reproduceerbare manier, zodat ze via een notebook future-proof kan worden opgenomen in de VSA Databricks-omgeving.

## 0.4. Aanpak

- We werken de data-analyse uit volgens de methodiek van het KMI: met de meest recente data doen we een replicatieonderzoek volgens de KMI/KNMI-benadering.
- We repliceren de regressieanalyse van VMM. Daarbij bespreken we de statistische beperkingen en toetsen we onder meer autocorrelatie omdat die relevant zijn voor de onzekerheid rond een enkelvoudige OLS-regressie.
- Ten slotte plaatsen we de resultaten naast elkaar. Dat is een kwaliteits- en methodenvergelijking, geen zelfstandig klimaatwetenschappelijk onderzoek. Waarbij we wel de richtlijnen voor tijdreeksanalyses en trend analyses in het kader van klimaatonderozek en communicatie hierover willen volgen.


# 1. Analyse vragen en data setup: "Extreme neerslag in Belgie: jaarlijkse maxima over 10 dagen"

## 1.1. Onderzoeksvragen

Deze notebook analyseert de jaarlijkse maximale neerslag over een periode van 10 opeenvolgende dagen. De focus ligt op drie vragen:

1. Hoe evolueert de volledige meetreeks doorheen de tijd? Is het methodologisch verdedigbaar om, zoals VMM doet, één globale OLS-regressie over de volledige meetperiode te gebruiken als hoofdboodschap voor de trend?. zie https://vmm.vlaanderen.be/feiten-cijfers/klimaat/klimaatthemas/wateroverlast-door-hevige-regenval/
2. Wat indien we de methodiek toepassen zoals deze in het klimaatrapport van het KMI is uitgewerkt en door het KMI gebruikt wordt. 
   Bijkomend: Is er sinds 1981 een recente lineaire trend, zoals in de KMI-klimaatrapportage vaak wordt gebruikt?
3. Is de conclusie over de trend gevoelig voor de keuze van de analyseperiode, bijvoorbeeld wanneer men enkel de periode vanaf 1981 of het laatste beschikbare 30-jarige venster bekijkt??

De analyse gebruikt de KMI/KNMI-Methodiek als leidraad: een gladde LOESS-curve voor de volledige reeks en een aparte recente trend vanaf 1981. Omdat extreme neerslag veel natuurlijke variabiliteit bevat, rapporteren we naast de schattingen ook robuuste onzekerheid en gevoeligheidschecks.


## 1.2. Setup en data

De ruwe Excel wordt (toegeleverd door VMM) omgezet naar een compacte CSV. Daarna werkt de rest van de notebook uitsluitend met `processed_max_neerslag.csv`, zodat de analyse reproduceerbaar en sneller uitvoerbaar blijft.
[noot: Nog aan te vullen: exacte bronvermelding van het aangeleverde Excel-bestand, datum van ontvangst, versie, contactpersoon en eventuele metadata over homogenisatie of berekeningswijze.]

***API-notitie***

De jaarlijkse puntdata voor extreme neerslag zoals opgenomen in de VOS en getoond op de websites van VMM en KMI zitten niet als kant-en-klare afgeleide klimaatindicator in de KMI Open Data API. De KMI Open Data API bevat wel ruwe neerslagwaarnemingen waarmee dergelijke indicatoren berekend kunnen worden. Als de exacte berekeningsregels en homogenisatiekeuzes beschikbaar zijn, kan de data-ingress in principe verder geautomatiseerd worden rechtstreeks uit de opendata API van het KMI.




## 2. Beschrijving van de reeks

We selecteren voor de verdere analyse enkel de 10 dagen reeks. Elk datapunt is het hoogste 10-daagse neerslagtotaal binnen een jaar. Het gaat dus om jaarlijkse maxima, niet om jaargemiddelden. Daardoor is de interjaarlijkse variabiliteit groot en moeten zowel trends als significantietoetsen voorzichtig worden geïnterpreteerd.



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Kenmerk</th>
      <th>Waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aantal jaren</td>
      <td>127</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Periode</td>
      <td>1898-2024</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Gemiddelde</td>
      <td>86.1 mm</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Mediaan</td>
      <td>84.6 mm</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Standaardafwijking</td>
      <td>19.8 mm</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Maximum</td>
      <td>158.8 mm</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Jaar van maximum</td>
      <td>1996</td>
    </tr>
  </tbody>
</table>
</div>



    
![png](neerslag_rapport_files/neerslag_rapport_6_1.png)
    


# 3. KMI / KNMI-methode

## 3.1. Methodologische samenvatting klimaatrapport KMI

In het KMI-klimaatrapport kan men de methodologie als volgt samenvatten wanneer we die plaatsen in de context van deze probleemstelling.

In dit KMI-klimaatrapport wordt voor waargenomen tijdreeksen een duidelijke tweesporenmethode gebruikt.

**1. Lange, gehomogeniseerde tijdreeksen**

Vooraleer trends worden berekend, benadrukt het KMI dat men klimaatverandering alleen zinvol kan analyseren met kwaliteitsvolle, voldoende lange en zo homogeen mogelijke tijdreeksen. Daarbij wordt gecorrigeerd voor niet-klimatologische breuken, zoals wijzigingen in meetstation, instrumenten, meetomgeving of waarnemingsprocedures. Zonder die stap kan een kunstmatige trend ontstaan die door meetomstandigheden komt en niet door klimaatverandering.

**2. Voor de grafieken systematisch twee technieken**

Het meest expliciet staat dit in het kader over de bepaling van klimatologische trends in de waarnemingen. Daarin worden twee technieken gecombineerd.

A. LOESS / lokale regressie als gladde trendcurve

Voor de volledige lange periode gebruikt men een gladde curve op de jaarlijkse waarden. Die vermindert de impact van interjaarlijkse variabiliteit en geeft een kwalitatief beeld van de meestal niet-lineaire evolutie over de hele periode. TR-389 beschrijft deze trendcurve technisch als lokale lineaire LOESS met tricubic gewichten over een venster van 42 jaar. De curve benadert inhoudelijk een 30-jaars lopend gemiddelde, maar met een lokale regressie in plaats van een eenvoudige gemiddeldewaarde.

B. Recente lineaire trends als aanvullende kwantificering

Het KMI-klimaatrapport gebruikt vaak een vaste recente referentieperiode vanaf 1981 om recente veranderingen te kwantificeren. Daarnaast kan een analyse van het laatste beschikbare 30-jarige venster nuttig zijn als gevoeligheidsanalyse, omdat 30 jaar aansluit bij de klassieke klimatologische referentieperiode. Dit laatste is echter niet hetzelfde als de TR-389-LOESS zelf.

**3. Wat bedoelt men met significant?**

In dit rapport is significantie niet overal exact hetzelfde criterium. Voor de Ukkel-grafieken wordt vaak een 90%-criterium gebruikt; voor ruimtelijke kaarten wordt eerder een 95%-significantieniveau gehanteerd. Daarom rapporteren we hier expliciet p-waarden en betrouwbaarheidsintervallen in plaats van alleen het label significant/niet significant.

Voor toetsing van verandering stelt het rapport niet voor om automatisch één globale regressie over de hele reeks te gebruiken.

**4. Welke methode is dus aanbevolen om klimaatverandering te beschrijven?**

Kort gezegd: voor detectie en beschrijving van klimaatverandering over lange tijd gebruikt men gehomogeniseerde lange tijdreeksen met LOESS/lokale regressie om de niet-lineaire evolutie zichtbaar te maken. Voor kwantificering van recente klimaatverandering gebruikt men een lineaire regressie vanaf een recente referentieperiode, met rapportering van helling, onzekerheid en significantie.

**5. Belangrijke nuance: OLS over de volledige eeuw is hoogstens een referentieanalyse**

Het KMI gebruikt geen eenvoudige globale lineaire regressie over de volledige beschikbare periode als hoofdboodschap voor klimaatverandering. In de TR-389-methodenvergelijking wordt een globale lineaire trend als minst geschikte algemene trendmethode gerangschikt voor lange klimaatreeksen, precies omdat ze één constante helling over de volledige periode veronderstelt.

Dat betekent niet dat een globale OLS-regressie rekenkundig fout is. Ze kan nuttig zijn als replicatie van de VMM-aanpak of als eenvoudige samenvattende referentie. Ze is alleen methodologisch te grof als hoofdboodschap voor een lange klimaatreeks.

**6. Inhoudelijke resultaten uit het rapport: voor temperatuur duidelijker dan voor neerslag**

Voor temperatuur concludeert het KMI ondubbelzinnig dat de seizoens- en jaartemperaturen sinds de 19e eeuw gestegen zijn, met een sterkere tweede opwarming vanaf het einde van de jaren 1980. Voor neerslag zijn de resultaten minder eenduidig, deels door de grotere natuurlijke variabiliteit. Daarom moet men voor neerslagextremen voorzichtiger zijn met sterke conclusies op basis van één model.

**7. Samenvatting**

De KMI/KNMI-benadering combineert homogenisatie, niet-lineaire trendvisualisatie met lokale lineaire LOESS en kwantificering van recente trends met lineaire regressie. LOESS beschrijft de vorm van de evolutie over de volledige periode zonder een constante trend te veronderstellen. De lineaire regressie vanaf 1981 rapporteert de recente verandering in interpreteerbare eenheden per decennium. Een globale OLS-trend over de volledige lange tijdreeks blijft nuttig als vergelijking met VMM, maar niet als enige klimaatboodschap.

## 3.2 Methodologisch referentiekader: KNMI TR-389 over klimatologische trendbepaling

et KNMI Technical Report TR-389, Standard method for determining a climatological trend, beschrijft een standaardmethode om klimatologische trends in tijdreeksen te bepalen voor reguliere KNMI-publicaties. Het rapport vertrekt van een belangrijke conceptuele definitie: een klimatologische trend is geen willekeurige regressielijn door alle waarnemingen, maar een representatie van de langetermijnverandering, waarbij kortetermijnfluctuaties door jaarlijkse weersvariabiliteit worden uitgefilterd. Een trend wordt in die benadering afgeleid uit een gladde trendlijn of smooth van de tijdreeks.

Het rapport vergelijkt verschillende mogelijke methoden om zo’n trendlijn te bepalen: het klassieke 30-jaars lopend gemiddelde, een globale lineaire regressie, GAM-smoothing en lokale polynomiale regressie of LOESS. Die methoden worden niet enkel beoordeeld op statistische elegantie, maar op een reeks praktische en klimatologisch relevante criteria: eenvoud, toepasbaarheid op verschillende klimaatvariabelen, lokaliteit in de tijd, flexibiliteit, aansluiting bij de klimatologische conventie van 30-jaarsgemiddelden, beperking van arbitraire keuzes en beschikbaarheid over de volledige periode.

In die vergelijking krijgt het klassieke 30-jaars lopend gemiddelde een sterke inhoudelijke positie, omdat het aansluit bij de klimatologische conventie. Het gemiddelde over een glijdend venster van 30 jaar dempt de jaarlijkse variabiliteit en geeft een herkenbare maat voor langetermijnverandering. Het nadeel is echter dat het niet goed gedefinieerd is aan het begin en vooral aan het einde van de tijdreeks: voor de recentste jaren ontbreken immers toekomstige waarnemingen om een gecentreerd 30-jaarsgemiddelde te berekenen. Daardoor is het klassieke 30-jaarsgemiddelde minder geschikt als operationele methode om de volledige reeks, inclusief de meest recente jaren, weer te geven.

Lineaire regressie wordt in TR-389 wel besproken als een eenvoudige methode, maar ze wordt methodologisch zwak beoordeeld als algemene methode voor klimatologische trendbepaling. De reden is niet dat lineaire regressie rekenkundig fout zou zijn. De reden is dat één globale rechte lijn over een lange tijdreeks een sterke vormaanname oplegt: de verandering wordt verondersteld constant lineair te verlopen over de volledige periode. Daardoor is de methode niet lokaal in de tijd, niet flexibel, en sluit ze niet goed aan bij de klimatologische conventie van 30-jaarsgemiddelden. Bovendien hangt de conclusie van zo’n globale regressie sterk af van het gekozen begin- en eindjaar. Een significante helling over de volledige reeks betekent dan vooral dat de gemiddelde lineaire helling over die hele historische periode van nul verschilt; ze zegt niet noodzakelijk dat er ook in de recente periode een duidelijke of significante stijging aanwezig is.

Als standaardmethode kiest TR-389 daarom voor een specifieke vorm van lokale lineaire regressie: een LOESS-trendlijn met tricubische gewichten over een venster van 42 jaar. Die keuze is niet arbitrair bedoeld, maar is afgestemd op de klimatologische 30-jaarsconventie. Door de tricubische weging is een breder venster nodig om ongeveer dezelfde variantie te bekomen als een ongewogen 30-jaarsgemiddelde. De methode wordt in het rapport samengevat als een “gladde trendlijn, bij benadering het 30-jaars lopend gemiddelde”. Technisch gaat het om lokale lineaire kleinste-kwadratenregressie met een tricubische weegfunctie over een 42-jaarsvenster.

Het belangrijke voordeel van deze LOESS-benadering is dat ze tegelijk lokaal, flexibel en klimatologisch interpreteerbaar is. Lokaal betekent dat de trendwaarde in een bepaald jaar alleen gebaseerd is op waarnemingen in een beperkte tijdsomgeving. Daardoor wordt vermeden dat zeer oude waarnemingen de interpretatie van recente evoluties blijven domineren. Flexibel betekent dat de trendlijn niet gedwongen wordt om één rechte lijn te zijn: versnellingen, vertragingen, plateaus of niet-lineaire evoluties kunnen zichtbaar worden. Klimatologisch interpreteerbaar betekent dat de methode dicht aansluit bij het vertrouwde 30-jaarsgemiddelde, maar zonder de praktische problemen aan het begin en einde van de reeks.

TR-389 maakt daarbij ook een belangrijk onderscheid tussen het weergeven van de volledige langetermijnevolutie en het toetsen van verandering. Voor de volledige reeks beveelt het rapport de LOESS-trendlijn aan. * Voor toetsing van verandering stelt het rapport niet voor om automatisch één globale regressie over de hele reeks te gebruiken.* De aanbevolen toetsing vertrekt van verschillen tussen twee vooraf gekozen, voldoende gescheiden jaren op de geschatte trendlijn. De gedachte daarachter is dat klimaatverandering niet noodzakelijk als één constante lineaire helling over de volledige meetperiode hoeft te verlopen. Een toets moet daarom aansluiten bij de trendlijn en bij een expliciete keuze van de periode waarover men verandering wil beoordelen.

In de context van deze evaluatie is dat onderscheid cruciaal. De VMM/VSA-benadering waarbij een lineaire regressie over de volledige neerslagreeks wordt toegepast, levert een statistisch berekenbare globale helling op. Die analyse beantwoordt echter een andere vraag dan de vraag die in klimaatrapportering centraal staat. Ze test of er gemiddeld over de volledige periode een lineaire stijging is, maar ze beschrijft niet noodzakelijk correct de vorm van de langetermijnevolutie en zegt weinig over de recentste klimaatevolutie. Voor een reeks zoals de maximale 10-daagse neerslag, die sterk varieert van jaar tot jaar en mogelijk niet-lineair evolueert, is die globale OLS-trend daarom beter te beschouwen als een aanvullende samenvatting, niet als hoofdindicator voor de klimatologische trend.

Een regressie op de laatste 30 jaar heeft een andere functie. Ze is geen vervanging van de TR-389-trendlijn, maar kan wel als aanvullende gevoeligheidsanalyse gebruikt worden. Omdat 30 jaar overeenkomt met de klassieke klimatologische referentieperiode, is een lineaire regressie over de recentste 30 jaar inhoudelijk beter verdedigbaar dan een regressie over de volledige historische reeks wanneer men specifiek de recente evolutie wil samenvatten. De interpretatie blijft echter beperkt: de geschatte helling zegt alleen iets over de gemiddelde lineaire verandering binnen dat recente venster. Bij neerslagextremen is de jaarlijkse variabiliteit groot, waardoor de onzekerheid rond zo’n helling vaak breed is. Een niet-significante trend over de laatste 30 jaar betekent dus niet dat er zeker geen verandering is, maar wel dat de beschikbare jaarwaarden binnen dat venster onvoldoende statistisch bewijs geven voor een duidelijke monotone lineaire stijging.

Voor deze nota betekent dit dat drie resultaten duidelijk uit elkaar moeten worden gehouden. Ten eerste is er de globale OLS-regressie over de volledige reeks: die kan significant positief zijn, maar is sterk modelafhankelijk en klimatologisch minder geschikt als hoofdconclusie. Ten tweede is er de LOESS-trendlijn volgens de TR-389-logica: die geeft de meest passende beschrijvende voorstelling van de langetermijnevolutie, omdat ze de 30-jaarsklimatologische conventie benadert en niet-lineaire evoluties toelaat. Ten derde is er de regressie over de recente periode, bijvoorbeeld vanaf 1981 of over de laatste 30 jaar: die is nuttig om de recente lineaire evolutie afzonderlijk te toetsen, maar moet met ruime onzekerheidsmarges en voorzichtige taal worden geïnterpreteerd.

## 3.3. Methodologische kernconclusie
De methodologische kernconclusie is dus niet dat lineaire regressie als techniek 'fout' is. De kern is dat één globale lineaire regressie over een lange klimaatreeks een te sterke en te weinig klimatologische modelkeuze is om als centrale trendboodschap te gebruiken. Een wetenschappelijk robuustere aanpak combineert een gladde lokale trendlijn voor de volledige reeks met een aparte, expliciet afgebakende analyse van recente verandering. Dat sluit beter aan bij de methodologische redenering van KNMI TR-389 en bij de manier waarop klimaatindicatoren voorzichtig moeten worden gecommuniceerd.

> ***Tegen deze methodologische achtergrond wordt hieronder nagegaan hoe de conclusie op basis van een globale OLS-regressie zich verhoudt tot een LOESS-gebaseerde beschrijving van de volledige reeks en tot een afzonderlijke trendanalyse voor de recente periode. Waarbij we 1981 als referentie gebruiken conform het KMI klimaatrapport en een venster van de laatste 30 jaar conform de het Technisch Rapport TR-389 over klimatologische trendbepaling van het KNMI. 
> We doen voor alle deze methoden een review en replicatie.***



## 3.2 KNMI/TR-389 LOESS: lokale lineaire trend met 42-jaarsvenster

Voor de volledige periode gebruiken we hier de KNMI/TR-389-benadering: lokale lineaire LOESS met een venster van 42 jaar en tricubic gewichten. In `statsmodels.lowess` betekent dit dat de fractie gelijk is aan `42 / n`. We zetten `it=0`, zodat er geen extra robuuste iteraties worden toegepast bovenop de lokale lineaire regressie.

Daarnaast tonen we een gecentreerd 30-jaars lopend gemiddelde. Dat is geen vervanging van de TR-389-LOESS, maar een inhoudelijke referentie omdat de LOESS-trendlijn volgens TR-389 ongeveer een 30-jaars lopend gemiddelde benadert.



    
![png](neerslag_rapport_files/neerslag_rapport_9_0.png)
    



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Jaar</th>
      <th>source_trend</th>
      <th>knmi_loess_python</th>
      <th>verschil_source_vs_python</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>127.000</td>
      <td>127.000</td>
      <td>127.000</td>
      <td>127.000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1961.000</td>
      <td>86.107</td>
      <td>85.847</td>
      <td>0.259</td>
    </tr>
    <tr>
      <th>std</th>
      <td>36.806</td>
      <td>5.151</td>
      <td>6.091</td>
      <td>3.261</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1898.000</td>
      <td>77.290</td>
      <td>70.019</td>
      <td>-4.619</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1929.500</td>
      <td>81.699</td>
      <td>83.161</td>
      <td>-2.860</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1961.000</td>
      <td>86.107</td>
      <td>85.083</td>
      <td>0.350</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1992.500</td>
      <td>90.515</td>
      <td>90.509</td>
      <td>2.626</td>
    </tr>
    <tr>
      <th>max</th>
      <td>2024.000</td>
      <td>94.923</td>
      <td>95.820</td>
      <td>7.489</td>
    </tr>
  </tbody>
</table>
</div>



    
![png](neerslag_rapport_files/neerslag_rapport_9_2.png)
    



    
![png](neerslag_rapport_files/neerslag_rapport_9_3.png)
    


## 3.3. Recente trend vanaf 1981 en laatste 30 jaar

De recente verandering wordt apart geschat met een lineaire trend vanaf 1981. Dat is een vaste recente referentieperiode, geen exact 30-jaarsvenster. Daarom tonen we daarnaast ook het laatste beschikbare 30-jaarsvenster. De helling wordt uitgedrukt in mm per decennium. De onzekerheid gebruikt HAC/Newey-West standaardfouten, zodat de p-waarde minder gevoelig is voor autocorrelatie en heteroskedasticiteit in de residualen.



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Periode</th>
      <th>n</th>
      <th>Trend</th>
      <th>90% BI</th>
      <th>p-waarde</th>
      <th>HAC maxlags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1981-2024</td>
      <td>44</td>
      <td>-1.47 mm/decennium</td>
      <td>-4.57 tot 1.62</td>
      <td>0,428</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1995-2024</td>
      <td>30</td>
      <td>-5.38 mm/decennium</td>
      <td>-11.15 tot 0.39</td>
      <td>0,124</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Methode</th>
      <th>Schatting</th>
      <th>Onzekerheid / toets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Lineaire trend vanaf 1981 met HAC-onzekerheid</td>
      <td>-1.47 mm/decennium</td>
      <td>90% BI -4.57 tot 1.62; p = 0,428</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Theil-Sen robuuste helling vanaf 1981</td>
      <td>-0.65 mm/decennium</td>
      <td>90% BI -3.80 tot 2.61 mm/decennium</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mann-Kendall monotone trend vanaf 1981</td>
      <td>tau = -0.041</td>
      <td>p = 0,701</td>
    </tr>
  </tbody>
</table>
</div>



    
![png](neerslag_rapport_files/neerslag_rapport_11_2.png)
    


## 3.4. Gevoeligheidsanalyse: startjaar van de lineaire trend

Deze gevoeligheidsanalyse toont hoe de geschatte lineaire trend verandert wanneer hetzelfde model telkens op een andere startperiode wordt toegepast. Een robuuste klimatologische conclusie mag niet uitsluitend afhangen van één toevallig gekozen startjaar.



    
![png](neerslag_rapport_files/neerslag_rapport_13_0.png)
    



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>startjaar</th>
      <th>eindjaar</th>
      <th>n</th>
      <th>trend_mm_per_decennium</th>
      <th>ci90_laag</th>
      <th>ci90_hoog</th>
      <th>p_waarde</th>
      <th>significant_90</th>
      <th>significant_95</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1898</td>
      <td>2024</td>
      <td>127</td>
      <td>1.399</td>
      <td>0.738</td>
      <td>2.059</td>
      <td>0.001</td>
      <td>True</td>
      <td>True</td>
    </tr>
    <tr>
      <th>53</th>
      <td>1951</td>
      <td>2024</td>
      <td>74</td>
      <td>1.711</td>
      <td>-0.058</td>
      <td>3.479</td>
      <td>0.111</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>63</th>
      <td>1961</td>
      <td>2024</td>
      <td>64</td>
      <td>0.910</td>
      <td>-1.759</td>
      <td>3.578</td>
      <td>0.571</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>73</th>
      <td>1971</td>
      <td>2024</td>
      <td>54</td>
      <td>0.752</td>
      <td>-1.897</td>
      <td>3.401</td>
      <td>0.637</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>83</th>
      <td>1981</td>
      <td>2024</td>
      <td>44</td>
      <td>-1.475</td>
      <td>-4.573</td>
      <td>1.624</td>
      <td>0.428</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>93</th>
      <td>1991</td>
      <td>2024</td>
      <td>34</td>
      <td>-5.083</td>
      <td>-9.742</td>
      <td>-0.423</td>
      <td>0.074</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>97</th>
      <td>1995</td>
      <td>2024</td>
      <td>30</td>
      <td>-5.380</td>
      <td>-11.153</td>
      <td>0.393</td>
      <td>0.124</td>
      <td>False</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>


**Interpretatie gevoeligheidsanalyse**

Deze gevoeligheidsanalyse toont dat de conclusie over een lineaire trend afhangt van de gekozen analyseperiode. De volledige reeks, en enkel deze, (1998-2024) geeft een positieve significante gemiddelde helling, maar de recente periode vanaf 1981 niet. Voor 1991-2024 vinden we zelf een negatief significant trend op .90 niveau. Dat bevestigt dat de globale OLS-trend vooral een modelmatige samenvatting over de volledige historische periode is, niet noodzakelijk een geschikte indicator voor de actuele klimaatevolutie.

Dit is ook de hoofdreden waarom LOESS benadering qua visualisatie van de trend eengewezen is en niet de voorstelling van een regressierechte voor de ganse poeriode. 



## 4. OLS regressie volledige reeks

### 4.1. Replicatie van VMM trend rechte
Als eenvoudige referentie schatten we voor de hele meetperiode een gewone OLS-regressie met een lineaire tijdtrend. Deze rechte lijn, alms zuivere replicatie van de VMM trend lijn, is vooral een samenvattende toets: ze laat zien of er gemiddeld over de volledige reeks een lineaire stijging of daling aanwezig is, terwijl de LOESS-curve daarnaast de niet-lineaire vorm van de evolutie blijft tonen.





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Parameter</th>
      <th>Schatting</th>
      <th>Std. fout</th>
      <th>t-waarde</th>
      <th>p-waarde</th>
      <th>CI95 laag</th>
      <th>CI95 hoog</th>
      <th>Eenheid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Intercept</td>
      <td>77.297</td>
      <td>3.386</td>
      <td>22.826</td>
      <td>&lt;0,001</td>
      <td>70.595</td>
      <td>83.999</td>
      <td>mm bij startjaar</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Trend</td>
      <td>1.399</td>
      <td>0.465</td>
      <td>3.011</td>
      <td>0,003</td>
      <td>0.479</td>
      <td>2.318</td>
      <td>mm/decennium</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Kenmerk</th>
      <th>Waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aantal jaren</td>
      <td>127</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Periode</td>
      <td>1898-2024</td>
    </tr>
    <tr>
      <th>2</th>
      <td>R-kwadraat</td>
      <td>0.067606</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Adjusted R-kwadraat</td>
      <td>0.060146</td>
    </tr>
    <tr>
      <th>4</th>
      <td>F-statistic p-waarde</td>
      <td>0,003</td>
    </tr>
    <tr>
      <th>5</th>
      <td>RMSE residualen (mm)</td>
      <td>19.04232</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Test</th>
      <th>Waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Durbin-Watson residualen</td>
      <td>2.002129</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Lag-1 autocorrelatie residualen</td>
      <td>-0.002953</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ljung-Box lag 10 p-waarde</td>
      <td>0,544</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Breusch-Pagan p-waarde</td>
      <td>0,390</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Shapiro-Wilk p-waarde</td>
      <td>&lt;0,001</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ljung-Box statistic</th>
      <th>p-waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0.0011</td>
      <td>0.9733</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2.0525</td>
      <td>0.8418</td>
    </tr>
    <tr>
      <th>10</th>
      <td>8.8798</td>
      <td>0.5435</td>
    </tr>
  </tbody>
</table>
</div>



    
![png](neerslag_rapport_files/neerslag_rapport_17_4.png)
    


## 4.2. Check van autocorrelatie

Een belangrijk reden om zeer voorzichtig te zijn met regressie analyses in het kader van tijdreeks analyse is de vereiste van onafhankelijkheid van de observaties. Een tijdsreeks is per definitie niet onafhankelijk. Dit heeft geen echte impact op de parameterschattingen maar wel op de schatting van de variantie. Die wordt met name onderschat, wat sneller tot type I fouten leidt, i.e. onterecht verwerpen van de O-hypothese. Met andere woorden onterecht besluiten dat er een significant verschil is. 

Het is echter mogelijk om dit te testen. Een eerste test is hierboven reeds uitgevoerd "Ljung-Box statistic". Deze is niet significant wat er op wijst dat autocorrelatie voor deze tijdsreeks geen isseu is. We visualiseren een extra check en doen dit hieronder op basis van 2 regressie technieken die expliciet de autoregressie als parameter opnemen, en door de klassieke testen van autocorrelatie toe te passen. 

### 4.2.1. Vergelijking: gewone OLS versus lineaire regressie met AR(1)-fouten



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>Intercept</th>
      <th>Trend (mm/decennium)</th>
      <th>Std. fout trend</th>
      <th>p-waarde trend</th>
      <th>CI95 trend laag</th>
      <th>CI95 trend hoog</th>
      <th>AR(1) rho</th>
      <th>R-kwadraat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>OLS volledige reeks</td>
      <td>77.297</td>
      <td>1.399</td>
      <td>0.465</td>
      <td>0,003</td>
      <td>0.479</td>
      <td>2.318</td>
      <td>NaN</td>
      <td>0.0676</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Regressie met AR(1)-fouten</td>
      <td>77.610</td>
      <td>1.362</td>
      <td>0.470</td>
      <td>0,004</td>
      <td>0.431</td>
      <td>2.292</td>
      <td>-0.0029</td>
      <td>0.0633</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>Test</th>
      <th>Waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>OLS volledige reeks</td>
      <td>F-test p-waarde</td>
      <td>0,003</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OLS volledige reeks</td>
      <td>Durbin-Watson</td>
      <td>2.002129</td>
    </tr>
    <tr>
      <th>2</th>
      <td>OLS volledige reeks</td>
      <td>Ljung-Box lag 10 p-waarde</td>
      <td>0,544</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Regressie met AR(1)-fouten</td>
      <td>Geschatte AR(1) rho</td>
      <td>-0.002911</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Regressie met AR(1)-fouten</td>
      <td>Durbin-Watson</td>
      <td>2.001992</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Regressie met AR(1)-fouten</td>
      <td>Ljung-Box lag 10 p-waarde</td>
      <td>0,545</td>
    </tr>
  </tbody>
</table>
</div>



    
![png](neerslag_rapport_files/neerslag_rapport_19_2.png)
    


Er zijn nauwelijks verschillen tussen beide methoden wat er op awijst dat de autocorrelatie mogelijk geen effect heeft op de betrouwbaarheidsiontervallen en de schatting van de standaardfout.

### 4.2.2. Vergelijking: gewone OLS versus OLS met HAC/Newey-West robuuste onzekerheid

HAC = heteroskedasticity and autocorrelation consistent. Newey-West corrigeert dus de standaardfouten voor:

-heteroskedasticiteit: ongelijke variantie van residuen;
-autocorrelatie: samenhang tussen residuen over naburige jaren.

In praktijk betekent dit vaak: dezelfde regressielijn, maar bredere betrouwbaarheidsintervallen en hogere p-waarden dan bij naïeve OLS, zeker als er positieve autocorrelatie zit in de residuen.

Bij tijdreeksen is de onzekerheid rond een geschatte trend niet alleen afhankelijk van de spreiding van de individuele residuen rond de regressielijn. Ook de samenhang tussen opeenvolgende residuen speelt een belangrijke rol. Wanneer residuen positief autocorreleren, betekent dit dat een positieve afwijking in het ene jaar vaak gevolgd wordt door een positieve afwijking in een volgend jaar, en omgekeerd. De observaties leveren dan minder onafhankelijke informatie dan wanneer elk jaar volledig los zou staan van de vorige jaren.

In klassieke OLS wordt de variantie van de schatter vooral gebaseerd op de variantie van de afzonderlijke residuen. Bij tijdreeksen is dat vaak te beperkt. De relevante variantie bevat niet alleen de gewone residuvariantie, maar ook de autocovarianties tussen residuen op verschillende tijdsafstanden. Schematisch kan men die zogenaamde langetermijnvariantie schrijven als:
$$γ0​+2γ1​+2γ2​+2γ3​+⋯$$

Daarbij staat γ0 voor de gewone variantie van de residuen. γ1 is de autocovariantie tussen residuen die één periode uit elkaar liggen, bijvoorbeeld tussen jaar t en jaar t−1. γ2 is de autocovariantie tussen residuen die twee jaren uit elkaar liggen, enzovoort... De termen worden met factor 2 opgenomen omdat de samenhang in beide richtingen meetelt: de covariantie tussen t en t−1 is dezelfde informatie als tussen t−1 en t.

De Newey-West-correctie probeert deze langetermijnvariantie te schatten. Ze doet dat niet door alle mogelijke autocovarianties onbeperkt mee te nemen, want dat zou bij een eindige tijdreeks te instabiel worden. In plaats daarvan wordt de som afgekapt na een gekozen aantal lags L. Alleen autocorrelatie tot en met die lag wordt dus meegenomen. Bovendien krijgen verder verwijderde lags een lager gewicht. Autocorrelatie tussen opeenvolgende jaren telt zwaarder mee dan autocorrelatie tussen jaren die verder uit elkaar liggen.

Daarom wordt HAC/Newey-West vaak beschreven als een schatter van de long-run variance. Dat is de variantie die relevant is wanneer observaties doorheen de tijd niet onafhankelijk zijn. In plaats van te doen alsof elk jaar een volledig nieuwe, onafhankelijke observatie is, houdt HAC rekening met het feit dat opeenvolgende jaren gedeeltelijk dezelfde onderliggende variatie kunnen delen.

Dit heeft directe gevolgen voor de standaardfout van de geschatte trendhelling. Stel dat de residuen positief autocorreleren:

$$
Cov(ut​,ut−1​)>0
$$

Dan bevatten bijvoorbeeld 120 jaarlijkse observaties minder onafhankelijke informatie dan 120 volledig onafhankelijke observaties. De effectieve steekproefgrootte is dan kleiner dan het nominale aantal jaren suggereert. Een gewone OLS-standaardfout houdt daar geen rekening mee en behandelt de 120 jaren alsof ze volledig onafhankelijk zijn. Daardoor wordt de onzekerheid rond de trendhelling vaak onderschat.

De HAC/Newey-West-correctie past dit aan. Ze laat de geschatte OLS-trend zelf ongemoeid, maar corrigeert de standaardfout van die trendhelling voor autocorrelatie en heteroskedasticiteit. Bij positieve autocorrelatie leidt dit vaak tot een grotere standaardfout, een breder betrouwbaarheidsinterval en een hogere p-waarde dan bij de klassieke OLS-berekening.

In formulevorm gaat het vaak van:
$$
SE(klassieke OLS​<SEHAC/Newey-West)​
$$

en dus meestal ook:
$$
p(klassieke OLS​<pHAC/Newey-West)​
$$

Dat is echter geen wiskundige garantie in elke toepassing. Het hangt af van de richting en sterkte van de autocorrelatie, de gekozen laglengte en de structuur van de residuen. Methodologisch is de hoofdboodschap dat HAC/Newey-West een robuustere onzekerheidsinschatting geeft dan naïeve OLS wanneer de data een tijdreeks vormen. De methode corrigeert dus de inferentie rond de trend, maar verandert niet het onderliggende model: het blijft een globale lineaire trend over de gekozen periode.

*Voor deze HAC/Newey-West-variantie die we gebruikten werd een maximale laglengte van 4 jaren gebruikt. Dit betekent dat autocovarianties tussen residuen tot en met vier jaar afstand worden meegenomen, met dalende Bartlett-gewichten. Deze keuze sluit aan bij gangbare vuistregels voor jaarlijkse tijdreeksen van ongeveer 120 observaties.*


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>Intercept</th>
      <th>Trend (mm/decennium)</th>
      <th>Std. fout trend</th>
      <th>t-waarde trend</th>
      <th>p-waarde trend</th>
      <th>CI95 trend laag</th>
      <th>CI95 trend hoog</th>
      <th>HAC maxlags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>OLS standaard</td>
      <td>77.297</td>
      <td>1.399</td>
      <td>0.465</td>
      <td>3.011</td>
      <td>0,003</td>
      <td>0.479</td>
      <td>2.318</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OLS HAC/Newey-West</td>
      <td>77.297</td>
      <td>1.399</td>
      <td>0.398</td>
      <td>3.511</td>
      <td>&lt;0,001</td>
      <td>0.610</td>
      <td>2.187</td>
      <td>4.0</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Kenmerk</th>
      <th>Waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aantal jaren</td>
      <td>127</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Periode</td>
      <td>1898-2024</td>
    </tr>
    <tr>
      <th>2</th>
      <td>R-kwadraat</td>
      <td>0.067606</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Durbin-Watson residualen</td>
      <td>2.002129</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ljung-Box lag 10 p-waarde</td>
      <td>0,544</td>
    </tr>
    <tr>
      <th>5</th>
      <td>HAC/Newey-West maxlags</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



    
![png](neerslag_rapport_files/neerslag_rapport_21_2.png)
    


Ook deze methodiek die op een meer robustere manier dan enkel een AR(1) schatting corrigeerd op de effecten van autocorrelatie zonder de punt schatting van de helling te beïnvloeden geeft geen verschillen met betrekking tot de vergelijking met een enkelvoudige regressie.

Daarbij dient men wel bij de interpretatie op te letten: 

**HAC of AR lost het hoofdprobleem van een globale lineaire trend over 120 jaar niet op. Ze corrigeren vooral de onzekerheid rond de regressiehelling bij autocorrelatie (en heteroscedasticiteit). Maar ze beantwoorden niet de vraag of één rechte lijn over de volledige klimaatperiode inhoudelijk een geschikt trendmodel is.**

## 4.2.3. Diagnostiek van de regressie vanaf 1981

We deden ook de test voor de de recente trend die we hierboven reeds uitvoerden. Deze is immers ook enkel betrouwbaar qua interferentie (sign test)  wanneer de residuen niet sterk gestructureerd/autocorrelatie vertonen. Daarom controleren we autocorrelatie expliciet met lag-1 autocorrelatie, Durbin-Watson en Ljung-Box tests.



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Diagnose</th>
      <th>Waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aantal jaren sinds 1981</td>
      <td>44.0000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>HAC maxlags</td>
      <td>3.0000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Lag-1 autocorrelatie residualen</td>
      <td>-0.0722</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Durbin-Watson residualen</td>
      <td>2.1360</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ljung-Box statistic</th>
      <th>p-waarde</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0.2431</td>
      <td>0.6220</td>
    </tr>
    <tr>
      <th>5</th>
      <td>7.8714</td>
      <td>0.1635</td>
    </tr>
    <tr>
      <th>10</th>
      <td>12.9023</td>
      <td>0.2292</td>
    </tr>
  </tbody>
</table>
</div>



    
![png](neerslag_rapport_files/neerslag_rapport_24_2.png)
    


**Interpretatie diagnostiek**

De diagnostiek geeft geen aanwijzing voor problematische autocorrelatie in de residualen van de recente regressie. De lag-1 autocorrelatie is klein en licht negatief (`-0,072`), terwijl een Durbin-Watsonwaarde van `2,14` dicht bij de referentiewaarde `2` ligt. Dat past bij residualen die niet systematisch jaar-op-jaar blijven doorwerken.

Ook de Ljung-Box tests blijven ruim boven de gebruikelijke 5%-grens (`p = 0,62` bij lag 1, `p = 0,16` bij lag 5 en `p = 0,23` bij lag 10). We verwerpen dus niet de nulhypothese dat de residualen geen autocorrelatie bevatten. De figuur ondersteunt dat beeld: de residualen schommelen rond nul zonder duidelijke opeenvolgende blokken of trend, al blijft de spreiding visueel niet perfect normaal.

Voor de trendinterpretatie betekent dit dat de lineaire regressie vanaf 1981 niet duidelijk wordt ondermijnd door autocorrelatie in de fouttermen. Het gebruik van HAC/Newey-West standaardfouten met `maxlags = 3` blijft wel zinvol als voorzichtige rapportagekeuze, omdat de steekproef beperkt is en jaarlijkse klimaatreeksen methodisch gevoelig kunnen zijn voor temporele afhankelijkheid.

Belangrijk: deze diagnostiek bewijst niet dat de oorspronkelijke neerslagreeks stationair is. Ze zegt alleen dat de residualen van dit recente lineaire model geen duidelijke autocorrelatiestructuur tonen. Voor stationariteit van de oorspronkelijke reeks zou een aparte tijdreeksanalyse nodig zijn.


# Conclusie

VMM gebruikt met OLS een statistisch herkenbare techniek, maar op de volledige reeks is die is niet dezelfde als de klimatologische analysemethodiek die KMI/KNMI als hoofdbenadering gebruiken voor lange klimaatreeksen.

In de klimatologische literatuur (o.a. KNMI TR-389) wordt afgeraden om lange klimaattijdreeksen uitsluitend met een globale lineaire trend te beschrijven. Dergelijke reeksen kunnen niet-lineaire evoluties en regimewissels vertonen. Daarom wordt aanbevolen om smoothing-technieken zoals LOESS te gebruiken voor de volledige periode en lineaire trends vooral te berekenen voor recente deelperiodes. 

De globale OLS-trend blijft in deze mogelijk nuttig als replicatie en vergelijking met de VMM-communicatie. Alhoewel één van de belangrijkste methodologische redenen om geen OLS regressie toe te passen op tijdreeksen, van uit de basis GAUSS-Markov voorwaarden voor OLS, de aanwezigheid van autocorrelatie is. Bleek dit na toetsing niet het geval. Dit neemt echter niet weg dat het toepassen hiervan voor het berekenen of communiceren een klimaattrends aangewezen is als good-practise . We konden dit vrij goed illuistreren op basis van gevoeligheidsanalyse van het startpunt van de regressie analyse.  

De hoofdinterpretatie moet  steunen op de combinatie van LOESS voor de vorm van de langetermijnevolutie te viosualiseren, en de recente trend van de laatste 30 jaar met expliciete onzekerheid, als diagnostiek van de recente trend. 

Verder vermeld de literatuur van klimatologisch onderzoek dat voor neerslagextremen terughoudendheid extra belangrijk is voor trendanalyses door de grote natuurlijke variabiliteit. Dit laatste toonden we wel degelijk aan op basis van een gevoeligheidsanalyse voor het startpunt mbt een regressierechte. 

we herhalen tot slot onze conclusie op basis van de literatuur:

> De methodologische kernconclusie is dus niet dat lineaire regressie als techniek 'fout' is. De kern is dat één globale lineaire regressie over een lange klimaatreeks een te sterke en te weinig klimatologische modelkeuze is om als centrale trendboodschap te gebruiken. Een wetenschappelijk robuustere aanpak combineert een gladde lokale trendlijn voor de volledige reeks met een aparte, expliciet afgebakende analyse van recente verandering. Dat sluit beter aan bij de methodologische redenering van KNMI TR-389 en bij de manier waarop klimaatindicatoren voorzichtig moeten worden gecommuniceerd.






