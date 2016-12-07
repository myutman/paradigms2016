select City.Name from
City inner join (Capital inner join Country
on (Capital.CountryCode == Country.Code) and (Country.Name == "Malaysia"))
on City.Id == Capital.CityId;

