select Country.Name, LiteracyRate.Rate from Country
inner join LiteracyRate on Country.Code == LiteracyRate.CountryCode
group by Country.Name
having max(LiteracyRate.Year)
order by LiteracyRate.Rate
limit 1;
