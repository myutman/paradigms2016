select City.Name, City.Population, Country.Population from City
inner join Country on City.CountryCode == Country.Code
order by (-City.Population * 1.0 / Country.Population), (-City.Name) desc
limit 20;
