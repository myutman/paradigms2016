select Country.Name from (Country
left outer join City on Country.Code == City.CountryCode)
group by Country.Name
having (2 * sum(City.Population) < Country.Population);

