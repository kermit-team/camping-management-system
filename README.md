# camping-management-system

Do instalacji aplikacji w kontenerze używamy komendy `bash /bin/dev_init.sh`

Podstawowa instancja aplikacji zawiera:
<ul>
    <li>
        3 grupy z przyznanymi odpowiednimi uprawnieniami:
        <ol>
            <li>Administratorzy</li>
            <li>Recepcjoniści</li>
            <li>Klienci</li>
        </ol>
    </li>
    <li>
        3 użytkowników:
        <ol>
            <li>Administrator o danych dostępowych: 
                admin@example.com admin</li>
            <li>Recepcjonista o danych dostępowych: 
                mateuszdwyk@gmail.com Q@werty123!</li>
            <li>Klient o danych dostępowych: 
                walasikszymon@gmail.com Q@werty123!</li>
        </ol>
    </li>
    <li>pola kempingowe</li>
    <li>2 rezerwacje użytkownika walasikszymon@gmail.com 
        (jedna opłacona, a druga anulowana)</li>
</ul>

W celu uruchomienia testów jednostkowych oraz lintera w backendzie
należy uruchomić komendę `bash /bin/dev_check.sh` posiadając uruchomioną
instancję kontenera aplikacji.

W celu wyczyszcenia danych w dockerze używamy komendy `bash /bin/dev_clear.sh`