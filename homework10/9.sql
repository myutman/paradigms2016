select First.Year, Second.Year, Country.Name, 1.0 * (Second.Rate - First.Rate) / (Second.Year - First.Year) Ave from Country
    inner join LiteracyRate First on First.CountryCode = Country.Code
    inner join LiteracyRate Second on (Second.Year - First.Year > 0 and First.CountryCode = Second.CountryCode)
group by First.Year, First.CountryCode
having min(Second.Year - First.Year)
order by Ave desc;
