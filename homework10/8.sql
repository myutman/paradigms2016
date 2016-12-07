select Country.Name, Country.Population, Country.SurfaceArea from Country
    inner join City on Country.Code = City.CountryCode
    inner join Capital on Country.Code = Capital.CountryCode
group by Country.Name
having max(City.Population) and (Capital.CityId <> City.Id)
order by (1.0 * Country.Population / Country.SurfaceArea) desc;
