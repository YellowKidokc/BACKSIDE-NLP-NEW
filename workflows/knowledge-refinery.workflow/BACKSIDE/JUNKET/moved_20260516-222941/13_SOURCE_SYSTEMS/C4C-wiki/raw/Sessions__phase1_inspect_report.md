# Phase 1 Source File Inspection


## books — `BibleData-Book.csv`

- rows: **66** | cols: **18**
- columns: `['book_name', 'hebrew_name', 'hebrew_transliteration', 'hebrew_meaning', 'greek_name', 'greek_transliteration', 'greek_meaning', 'chapter_count', 'verse_count', 'book_id', 'christian_sequence', 'hebrew_sequence', 'short_name', 'usx_code', 'writer_id', 'written_start_date', 'written_end_date', 'written_location_id']`
- dtypes:
  - `book_name`: object  (66 non-null)
  - `hebrew_name`: object  (39 non-null)
  - `hebrew_transliteration`: object  (39 non-null)
  - `hebrew_meaning`: object  (39 non-null)
  - `greek_name`: object  (66 non-null)
  - `greek_transliteration`: object  (66 non-null)
  - `greek_meaning`: object  (15 non-null)
  - `chapter_count`: int64  (66 non-null)
  - `verse_count`: int64  (66 non-null)
  - `book_id`: int64  (66 non-null)
  - `christian_sequence`: int64  (66 non-null)
  - `hebrew_sequence`: int64  (66 non-null)
  - `short_name`: object  (66 non-null)
  - `usx_code`: object  (66 non-null)
  - `writer_id`: object  (6 non-null)
  - `written_start_date`: float64  (6 non-null)
  - `written_end_date`: float64  (0 non-null)
  - `written_location_id`: float64  (0 non-null)
- sample (3 rows):
```
   book_name hebrew_name hebrew_transliteration    hebrew_meaning greek_name greek_transliteration   greek_meaning  chapter_count  verse_count  book_id  christian_sequence  hebrew_sequence short_name usx_code writer_id  written_start_date  written_end_date  written_location_id
0    Genesis      בּראשׁית               Bereshit  In the Beginning    Γένεσις               Genesis       Beginning             50         1533        1                   1                1        Gen      GEN   Moses_1             -1476.0               NaN                  NaN
1     Exodus        שׁמוֹת                 Shemot             Names     Ἔξοδος                Exodus       Departure             40         1213        2                   2                2       Exod      EXO   Moses_1             -1475.0               NaN                  NaN
2  Leviticus       ויקרא                Vayikra     And He Called  Λευϊτικόν             Leuitikon  Of the Levites             27          859        3                   3                3        Lev      LEV   Moses_1             -1475.0               NaN                  NaN
```

## chapters — `Chapters.csv`

- rows: **1,189** | cols: **10**
- columns: `['osisRef', 'book', 'chapterNum', 'writer', 'verses', 'slug', 'peopleCount', 'placesCount', 'modified', 'writer count']`
- dtypes:
  - `osisRef`: object  (1,189 non-null)
  - `book`: object  (1,189 non-null)
  - `chapterNum`: int64  (1,189 non-null)
  - `writer`: object  (1,132 non-null)
  - `verses`: object  (1,189 non-null)
  - `slug`: object  (1,189 non-null)
  - `peopleCount`: int64  (1,189 non-null)
  - `placesCount`: int64  (1,189 non-null)
  - `modified`: object  (1,189 non-null)
  - `writer count`: int64  (1,189 non-null)
- sample (3 rows):
```
   osisRef  book  chapterNum       writer                                   verses     slug  peopleCount  placesCount          modified  writer count
0   1Sam.1  1Sam           1  samuel_2469  1Sam.1.1,1Sam.1.2,1Sam.1.3,1Sam.1.4,...   1sam_1           26            5  2020-08-07 13:12             1
1  1Sam.13  1Sam          13  samuel_2469  1Sam.13.1,1Sam.13.2,1Sam.13.3,1Sam.1...  1sam_13           15           13  2020-08-07 13:12             1
2  1Sam.19  1Sam          19  samuel_2469  1Sam.19.1,1Sam.19.2,1Sam.19.3,1Sam.1...  1sam_19           22            4  2020-08-07 13:12             1
```

## verses — `Verses.csv`

- rows: **31,102** | cols: **18**
- columns: `['osisRef', 'status', 'verseID', 'book', 'chapter', 'verseNum', 'verseText', 'richText', 'mdText', 'people', 'peopleCount', 'places', 'placesCount', 'yearNum', 'peopleGroups', 'eventsDescribed', 'timeline', 'modified']`
- dtypes:
  - `osisRef`: object  (31,102 non-null)
  - `status`: object  (31,102 non-null)
  - `verseID`: int64  (31,102 non-null)
  - `book`: object  (31,102 non-null)
  - `chapter`: object  (31,102 non-null)
  - `verseNum`: int64  (31,102 non-null)
  - `verseText`: object  (31,102 non-null)
  - `richText`: object  (31,102 non-null)
  - `mdText`: object  (31,102 non-null)
  - `people`: object  (16,513 non-null)
  - `peopleCount`: int64  (31,102 non-null)
  - `places`: object  (4,811 non-null)
  - `placesCount`: int64  (31,102 non-null)
  - `yearNum`: float64  (28,024 non-null)
  - `peopleGroups`: object  (13 non-null)
  - `eventsDescribed`: object  (1,240 non-null)
  - `timeline`: object  (13,388 non-null)
  - `modified`: object  (31,102 non-null)
- sample (3 rows):
```
   osisRef   status  verseID book chapter  verseNum                                verseText                                 richText                                   mdText                     people  peopleCount places  placesCount  yearNum peopleGroups         eventsDescribed                timeline        modified
0  Gen.1.1  publish  1001001  Gen   Gen.1         1  In the beginning God created the hea...  In the beginning God created the hea...  In the beginning [God]([/person/god_...                   god_1324            1    NaN            0  -4004.0          NaN  God creates all things  Creation of all things  1/8/2021 15:07
1  Gen.1.2  publish  1001002  Gen   Gen.1         2  And the earth was without form, and ...  And the earth was without form, and ...  And the earth was without form, and ...  god_1324,holy_spirit_7400            2    NaN            0  -4004.0          NaN  God creates all things  Creation of all things  1/8/2021 15:07
2  Gen.1.3  publish  1001003  Gen   Gen.1         3  And God said, Let there be light: an...  And God said, Let there be light: an...  And [God]([/person/god_1324) said, L...                   god_1324            1    NaN            0  -4004.0          NaN  God creates all things  Creation of all things  1/8/2021 15:07
```

## timeline — `Bible Timeline.csv`

- rows: **584** | cols: **1**
- columns: `['So I I ,Column2,Column3']`
- dtypes:
  - `So I I ,Column2,Column3`: object  (584 non-null)
- sample (3 rows):
```
                   So I I ,Column2,Column3
0  Before Time,In the Beginning was the...
1    Before 4000 BC,The Creation,Genesis 1
2  Before 4000 BC,The Garden of Eden,Ge...
```

## periods — `Periods.csv`

- rows: **250** | cols: **10**
- columns: `['yearNum', 'formattedYear', 'era', 'isoYear', 'BC-AD', 'peopleBorn', 'peopleDied', 'events', 'booksWritten', 'modified']`
- dtypes:
  - `yearNum`: int64  (250 non-null)
  - `formattedYear`: object  (250 non-null)
  - `era`: float64  (0 non-null)
  - `isoYear`: int64  (250 non-null)
  - `BC-AD`: object  (250 non-null)
  - `peopleBorn`: object  (69 non-null)
  - `peopleDied`: object  (59 non-null)
  - `events`: object  (28 non-null)
  - `booksWritten`: object  (11 non-null)
  - `modified`: object  (250 non-null)
- sample (3 rows):
```
   yearNum formattedYear  era  isoYear BC-AD        peopleBorn peopleDied                                   events booksWritten          modified
0    -4004       4004 BC  NaN    -4003    BC  adam_78,eve_1231        NaN  God creates all things,God creates m...          NaN  2020-05-15 01:02
1    -3941       3941 BC  NaN    -3940    BC               NaN        NaN                                      NaN          NaN  2019-07-22 00:52
2    -3939       3939 BC  NaN    -3938    BC               NaN        NaN                                      NaN          NaN  2020-05-15 01:08
```

## epochs — `BibleData-Epoch.csv`

- rows: **999** | cols: **15**
- columns: `['epoch_id', 'epoch_name', 'epoch_description', 'epoch_type', 'person_id', 'start_year_ah', 'end_year_ah', 'period_length', 'start_year_calculation', 'start_year_offset', 'start_year_reference_id', 'end_year_calculation', 'end_year_reference_id', 'period_length_reference_id', 'epoch_notes']`
- dtypes:
  - `epoch_id`: object  (159 non-null)
  - `epoch_name`: object  (159 non-null)
  - `epoch_description`: object  (159 non-null)
  - `epoch_type`: object  (159 non-null)
  - `person_id`: object  (34 non-null)
  - `start_year_ah`: float64  (39 non-null)
  - `end_year_ah`: float64  (37 non-null)
  - `period_length`: float64  (37 non-null)
  - `start_year_calculation`: object  (36 non-null)
  - `start_year_offset`: float64  (30 non-null)
  - `start_year_reference_id`: object  (33 non-null)
  - `end_year_calculation`: object  (36 non-null)
  - `end_year_reference_id`: object  (1 non-null)
  - `period_length_reference_id`: object  (32 non-null)
  - `epoch_notes`: object  (4 non-null)
- sample (3 rows):
```
      epoch_id        epoch_name                        epoch_description epoch_type person_id  start_year_ah  end_year_ah  period_length                   start_year_calculation  start_year_offset start_year_reference_id                     end_year_calculation end_year_reference_id period_length_reference_id                       epoch_notes
0     Creation      The Creation  All of Creation was formed by G-d's ...     Unique     G-d_1            1.0          NaN            NaN                                      NaN                NaN                     NaN                                      NaN                   NaN                        NaN  Seven days of creation (GEN 2:2)
1  Life_Adam_1  The Life of Adam  God created man in His own image, in...       Life    Adam_1            1.0        931.0          930.0                                      NaN                NaN                GEN 1:27  Adam_1 birth year (1) + Adam_1 age a...                   NaN                    GEN 5:5                               NaN
2  Life_Seth_1  The Life of Seth  When Adam had lived one hundred and ...       Life    Seth_1          131.0       1043.0          912.0  Birth year of father (1) + age of fa...              130.0                 GEN 5:3  Seth_1 birth year (131) + Seth_1 age...                   NaN                    GEN 5:8                               NaN
```

## events_bd — `BibleData-Event.csv`

- rows: **999** | cols: **27**
- columns: `['event_id', 'event_label', 'event_description', 'event_type', 'person_id', 'event_year_ah', 'person_age_at_event', 'event_year_offset', 'event_reference_id', 'event_year_calculation', 'event_location', 'event_location_reference_id', 'event_notes', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26']`
- dtypes:
  - `event_id`: object  (210 non-null)
  - `event_label`: object  (210 non-null)
  - `event_description`: object  (193 non-null)
  - `event_type`: object  (210 non-null)
  - `person_id`: object  (171 non-null)
  - `event_year_ah`: float64  (173 non-null)
  - `person_age_at_event`: float64  (127 non-null)
  - `event_year_offset`: float64  (136 non-null)
  - `event_reference_id`: object  (169 non-null)
  - `event_year_calculation`: object  (172 non-null)
  - `event_location`: object  (67 non-null)
  - `event_location_reference_id`: object  (60 non-null)
  - `event_notes`: object  (101 non-null)
  - `Unnamed: 13`: float64  (0 non-null)
  - `Unnamed: 14`: float64  (0 non-null)
  - `Unnamed: 15`: float64  (0 non-null)
  - `Unnamed: 16`: float64  (0 non-null)
  - `Unnamed: 17`: float64  (0 non-null)
  - `Unnamed: 18`: float64  (0 non-null)
  - `Unnamed: 19`: float64  (0 non-null)
  - `Unnamed: 20`: float64  (0 non-null)
  - `Unnamed: 21`: float64  (0 non-null)
  - `Unnamed: 22`: float64  (0 non-null)
  - `Unnamed: 23`: float64  (0 non-null)
  - `Unnamed: 24`: float64  (0 non-null)
  - `Unnamed: 25`: float64  (0 non-null)
  - `Unnamed: 26`: float64  (0 non-null)
- sample (3 rows):
```
       event_id    event_label                        event_description event_type person_id  event_year_ah  person_age_at_event  event_year_offset event_reference_id                   event_year_calculation event_location event_location_reference_id                              event_notes  Unnamed: 13  Unnamed: 14  Unnamed: 15  Unnamed: 16  Unnamed: 17  Unnamed: 18  Unnamed: 19  Unnamed: 20  Unnamed: 21  Unnamed: 22  Unnamed: 23  Unnamed: 24  Unnamed: 25  Unnamed: 26
0      Creation   The Creation  All of Creation was formed by G-d's ...     Unique     G-d_1            1.0                  NaN                NaN                NaN                                      NaN            NaN                         NaN         Seven days of creation (GEN 2:2)          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN
1  Birth_Adam_1  Birth of Adam  God created man in His own image, in...      Birth    Adam_1            1.0                  0.0                NaN           GEN 1:27    No calculation: fundamental assertion   West of Eden                     GEN 2:8  Adam was created (not born) on the 6...          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN
2  Birth_Seth_1  Birth of Seth  When Adam had lived ONE HUNDRED AND ...      Birth    Seth_1          131.0                  0.0              130.0            GEN 5:3  Birth year of Seth_1's father [Adam_...            NaN                         NaN                                      NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN          NaN
```

## events_plain — `Events.csv`

- rows: **395** | cols: **19**
- columns: `['title', 'ID', 'startDate', 'duration', 'rangeFlag', 'predecessor', 'lag', 'Lag Type', 'partOf', 'verses', 'people (from verses)', 'participants', 'places (from verses)', 'locations', 'groups', 'notes', 'verseSort', 'modified', 'Sort Key']`
- dtypes:
  - `title`: object  (395 non-null)
  - `ID`: int64  (395 non-null)
  - `startDate`: object  (395 non-null)
  - `duration`: object  (395 non-null)
  - `rangeFlag`: object  (6 non-null)
  - `predecessor`: object  (337 non-null)
  - `lag`: object  (88 non-null)
  - `Lag Type`: object  (88 non-null)
  - `partOf`: object  (184 non-null)
  - `verses`: object  (395 non-null)
  - `people (from verses)`: object  (392 non-null)
  - `participants`: object  (381 non-null)
  - `places (from verses)`: object  (239 non-null)
  - `locations`: object  (256 non-null)
  - `groups`: object  (41 non-null)
  - `notes`: object  (2 non-null)
  - `verseSort`: int64  (395 non-null)
  - `modified`: object  (395 non-null)
  - `Sort Key`: float64  (395 non-null)
- sample (3 rows):
```
                      title  ID startDate duration rangeFlag               predecessor  lag Lag Type                                   partOf                                   verses                     people (from verses)                         participants                     places (from verses) locations groups notes  verseSort           modified    Sort Key
0    Creation of all things   1     -4003       6D       NaN                       NaN  NaN      NaN                                      NaN  Gen.1.1,Gen.1.2,Gen.1.3,Gen.1.4,Gen....  god_1324,god_1324,holy_spirit_7400,g...  god_1324,jesus_905,holy_spirit_7400                                      NaN       NaN    NaN   NaN    1001001  11/25/2020 9:12am -4002.98999
1  Creation of Adam and Eve   2     -4003       1D       NaN                       NaN  NaN      NaN  Lifetime of Adam,Creation of Adam an...  Gen.2.4,Gen.2.5,Gen.2.6,Gen.2.7,Gen....  god_1324,god_1324,god_1324,god_1324,...            adam_78,eve_1231,god_1324  eden_354,eden_354,havilah_533,pishon...  eden_354    NaN   NaN    1002004  11/25/2020 9:12am -4002.98998
2                  The Fall   3     -4003       1D   checked  Creation of Adam and Eve  NaN      NaN                                      NaN  Gen.3.1,Gen.3.2,Gen.3.3,Gen.3.4,Gen....  god_1324,god_1324,god_1324,adam_78,g...            adam_78,eve_1231,god_1324                        eden_354,eden_354  eden_354    NaN   NaN    1003001  11/25/2020 9:12am -4002.98997
```

## persons — `BibleData-Person.csv`

- rows: **3,009** | cols: **9**
- columns: `['person_id', 'person_name', 'surname', 'unique_attribute', 'sex', 'tribe', 'person_notes', 'name_instance', 'person_sequence']`
- dtypes:
  - `person_id`: object  (3,009 non-null)
  - `person_name`: object  (3,009 non-null)
  - `surname`: object  (8 non-null)
  - `unique_attribute`: object  (3,009 non-null)
  - `sex`: object  (3,009 non-null)
  - `tribe`: object  (1,608 non-null)
  - `person_notes`: object  (674 non-null)
  - `name_instance`: int64  (3,009 non-null)
  - `person_sequence`: int64  (3,009 non-null)
- sample (3 rows):
```
  person_id person_name surname                         unique_attribute     sex tribe person_notes  name_instance  person_sequence
0    YHVH_1        YHVH     NaN  Holy, Holy, Holy (ISA 6:3) and too m...    male   NaN          NaN              1                1
1    Adam_1        Adam     NaN                    first man (1CO 15:45)    male   NaN          NaN              1                2
2     Eve_1         Eve     NaN  first woman, created from Adam (GEN ...  female   NaN          NaN              1                3
```

## persons_detail — `People.csv`

- rows: **3,069** | cols: **36**
- columns: `['personLookup', 'status', 'personID', 'displayTitle', 'name', 'surname', 'alsoCalled', 'isProperName', 'ambiguous', 'Disambiguation (temp)', 'gender', 'occupations', 'birthYear', 'minYear', 'deathYear', 'maxYear', 'birthPlace', 'deathPlace', 'memberOf', 'eastons', 'dictText', 'events', 'eventGroups', 'verseCount', 'verses', 'mother', 'father', 'partners', 'children', 'siblings', 'halfSiblingsSameMother', 'halfSiblingsSameFather', 'chaptersWritten', 'alphaGroup', 'slug', 'modified']`
- dtypes:
  - `personLookup`: object  (3,069 non-null)
  - `status`: object  (3,069 non-null)
  - `personID`: int64  (3,069 non-null)
  - `displayTitle`: object  (3,069 non-null)
  - `name`: object  (3,069 non-null)
  - `surname`: object  (14 non-null)
  - `alsoCalled`: object  (351 non-null)
  - `isProperName`: object  (3,044 non-null)
  - `ambiguous`: object  (1,613 non-null)
  - `Disambiguation (temp)`: object  (1,707 non-null)
  - `gender`: object  (3,069 non-null)
  - `occupations`: float64  (0 non-null)
  - `birthYear`: float64  (75 non-null)
  - `minYear`: int64  (3,069 non-null)
  - `deathYear`: float64  (64 non-null)
  - `maxYear`: int64  (3,069 non-null)
  - `birthPlace`: object  (77 non-null)
  - `deathPlace`: object  (45 non-null)
  - `memberOf`: object  (736 non-null)
  - `eastons`: object  (1,817 non-null)
  - `dictText`: object  (1,817 non-null)
  - `events`: object  (108 non-null)
  - `eventGroups`: object  (108 non-null)
  - `verseCount`: int64  (3,069 non-null)
  - `verses`: object  (3,067 non-null)
  - `mother`: object  (200 non-null)
  - `father`: object  (1,584 non-null)
  - `partners`: object  (173 non-null)
  - `children`: object  (963 non-null)
  - `siblings`: object  (944 non-null)
  - `halfSiblingsSameMother`: object  (3 non-null)
  - `halfSiblingsSameFather`: object  (111 non-null)
  - `chaptersWritten`: object  (39 non-null)
  - `alphaGroup`: object  (3,069 non-null)
  - `slug`: object  (3,069 non-null)
  - `modified`: object  (3,069 non-null)
- sample (3 rows):
```
  personLookup   status  personID displayTitle     name surname alsoCalled isProperName ambiguous Disambiguation (temp) gender  occupations  birthYear  minYear  deathYear  maxYear birthPlace     deathPlace       memberOf  eastons                                 dictText events eventGroups  verseCount                                   verses         mother     father       partners                                 children                siblings halfSiblingsSameMother halfSiblingsSameFather chaptersWritten alphaGroup       slug          modified
0      aaron_1  publish         1        Aaron    Aaron     NaN        NaN      checked       NaN                   NaN   Male          NaN    -1574.0    -1700    -1451.0       64  egypt_362  mount_hor_842  Tribe of Levi    Aaron  The eldest son of Amram and Jochebed...    NaN         NaN         331  Exod.4.14,Exod.4.27,Exod.4.28,Exod.4...  jochebed_1645  amram_242  elisheba_1162  abihu_33,eleazar_1062,nadab_2128,ith...  miriam_2087,moses_2108                    NaN                    NaN             NaN          A    aaron_1  2020-09-07 19:30
1    abagtha_3      wip         3      Abagtha  Abagtha     NaN        NaN      checked       NaN                   NaN   Male          NaN        NaN     -462        NaN     -462        NaN            NaN            NaN  Abagtha  One of the seven eunuchs in Ahasueru...    NaN         NaN           1                                Esth.1.10            NaN        NaN            NaN                                      NaN                     NaN                    NaN                    NaN             NaN          A  abagtha_3  2019-07-27 11:49
2       abda_4      wip         4         Abda     Abda     NaN        NaN      checked       NaN                   NaN   Male          NaN        NaN    -1014        NaN    -1014        NaN            NaN            NaN   Abda 1  The father of Adoniram, whom Solomon...    NaN         NaN           1                                 1Kgs.4.6            NaN        NaN            NaN                             adoniram_102                     NaN                    NaN                    NaN             NaN          A     abda_4  2019-07-27 11:49
```

## pv_general — `BibleData-PersonVerse.csv`

- rows: **44,267** | cols: **8**
- columns: `['person_verse_id', 'reference_id', 'person_label_id', 'person_id', 'person_label', 'person_label_count', 'person_verse_sequence', 'person_verse_notes']`
- dtypes:
  - `person_verse_id`: object  (44,267 non-null)
  - `reference_id`: object  (44,267 non-null)
  - `person_label_id`: object  (29,534 non-null)
  - `person_id`: object  (29,534 non-null)
  - `person_label`: object  (29,534 non-null)
  - `person_label_count`: float64  (29,534 non-null)
  - `person_verse_sequence`: int64  (44,267 non-null)
  - `person_verse_notes`: object  (4,761 non-null)
- sample (3 rows):
```
     person_verse_id reference_id person_label_id person_id person_label  person_label_count  person_verse_sequence person_verse_notes
0  GEN 1:1__YHVH_1_1      GEN 1:1        YHVH_1_1    YHVH_1          G-d                 1.0                      1                NaN
1  GEN 1:2__YHVH_1_1      GEN 1:2        YHVH_1_1    YHVH_1          G-d                 1.0                      2                NaN
2  GEN 1:3__YHVH_1_1      GEN 1:3        YHVH_1_1    YHVH_1          G-d                 1.0                      3                NaN
```

## pv_apostolic — `BibleData-PersonVerse-Apostolic.csv`

**MISSING** — file not found at `C:\Users\lowes\Desktop\Bible Studies E xcel-20251109T142609Z-1-001\Bible Studies E xcel\BibleData-PersonVerse-Apostolic.csv`


## pv_tanakh — `BibleData-PersonVerse-Tanakh.csv`

**MISSING** — file not found at `C:\Users\lowes\Desktop\Bible Studies E xcel-20251109T142609Z-1-001\Bible Studies E xcel\BibleData-PersonVerse-Tanakh.csv`


## people_groups — `PeopleGroups.csv`

- rows: **20** | cols: **7**
- columns: `['groupName', 'members', 'partOf', 'verses', 'events', 'modified', 'events_dev']`
- dtypes:
  - `groupName`: object  (20 non-null)
  - `members`: object  (17 non-null)
  - `partOf`: object  (8 non-null)
  - `verses`: object  (2 non-null)
  - `events`: object  (2 non-null)
  - `modified`: object  (19 non-null)
  - `events_dev`: object  (18 non-null)
- sample (3 rows):
```
           groupName                                  members partOf verses events          modified                               events_dev
0      Tribe of Levi  aaron_1,abdi_6,abiah_15,abihu_33,abi...    NaN    NaN    NaN  2020-09-07 20:00  Exodus from Egypt,Wilderness Wanderi...
1  Tribe of Benjamin  abiah_17,abihud_34,abishua_52,addar_...    NaN    NaN    NaN  2020-09-07 20:00  Exodus from Egypt,Wilderness Wanderi...
2    Tribe of Joseph  abiezer_763,ahian_130,ammihud_223,an...    NaN    NaN    NaN  2020-09-07 20:00  Exodus from Egypt,Wilderness Wanderi...
```

## DEDUP ANALYSIS

### persons vs persons_detail overlap
- `BibleData-Person.csv`: 3,009 rows, cols: ['person_id', 'person_name', 'surname', 'unique_attribute', 'sex', 'tribe', 'person_notes', 'name_instance', 'person_sequence']
- `People.csv`: 3,069 rows, cols: ['personLookup', 'status', 'personID', 'displayTitle', 'name', 'surname', 'alsoCalled', 'isProperName', 'ambiguous', 'Disambiguation (temp)']
- potential ID cols (p1): ['person_id', 'person_name', 'person_notes', 'person_sequence']
- potential ID cols (p2): ['personLookup', 'personID']

### PersonVerse trio overlap
- `BibleData-PersonVerse.csv`: 44,267 rows, cols: ['person_verse_id', 'reference_id', 'person_label_id', 'person_id', 'person_label', 'person_label_count', 'person_verse_sequence', 'person_verse_notes']
- ERROR: [Errno 2] No such file or directory: 'C:\\Users\\lowes\\Desktop\\Bible Studies E xcel-20251109T142609Z-1-001\\Bible Studies E xcel\\BibleData-PersonVerse-Apostolic.csv'

### Events dedup (BibleData-Event.csv vs Events.csv)
- `BibleData-Event.csv`: 999 rows, cols: ['event_id', 'event_label', 'event_description', 'event_type', 'person_id', 'event_year_ah', 'person_age_at_event', 'event_year_offset', 'event_reference_id', 'event_year_calculation', 'event_location', 'event_location_reference_id', 'event_notes', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26']
- `Events.csv`: 395 rows, cols: ['title', 'ID', 'startDate', 'duration', 'rangeFlag', 'predecessor', 'lag', 'Lag Type', 'partOf', 'verses', 'people (from verses)', 'participants', 'places (from verses)', 'locations', 'groups', 'notes', 'verseSort', 'modified', 'Sort Key']

## KJ SCHEMA CONVENTIONS (for matching)

### kj.verses
- `verse_euid`: text
- `book_code`: text
- `book_number`: integer
- `chapter`: integer
- `verse`: integer
- `verse_text`: text
- `word_count`: integer
- `created_at`: timestamp without time zone
sample: ('GN-001-001', 'GN', 1, 1, 1, 'In the beginning God created the heaven and the earth.', 10, datetime.datetime(2025, 11, 17, 6, 6, 2, 609656))

### kj.book_codes
- `book_number`: integer
- `book_code`: text
- `book_name`: text
- `testament`: text
sample: (1, 'GN', 'Genesis', 'OLD_TESTAMENT')

### kj.people
- `person_euid`: text
- `person_id`: text
- `person_name`: text
- `surname`: text
- `unique_attribute`: text
- `sex`: text
- `tribe`: text
- `person_notes`: text
- `name_instance`: integer
- `person_sequence`: integer
- `created_at`: timestamp without time zone
sample: ('PS-YHVH_1', 'YHVH_1', 'YHVH', 'NaN', 'Holy, Holy, Holy (ISA 6:3) and too many others to fit here', 'male', 'NaN', 'NaN', 1, 1, datetime.datetime(2025, 11, 17, 6, 37, 51, 619716))

### kj.places
- `place_euid`: text
- `place_id`: text
- `place_name`: text
- `place_type`: text
- `modern_equivalent`: text
- `place_notes`: text
- `openbible_id`: text
- `openbible_url`: text
- `name_instance`: integer
- `place_sequence`: integer
- `created_at`: timestamp without time zone
sample: ('PL-heaven_1', 'heaven_1', 'heaven', 'astronomical', 'the universe', 'the abode of stars (GEN 15:5, DEU 4:19, PSA 8:3, etc.)', 'none', None, 1, 1, datetime.datetime(2025, 11, 17, 8, 0, 23, 776824))
