def valid_email():
    query='''
        select distinct email from SampleDataValidation 
        where email like '%@%.com' 
    '''
    return query

def invalid_email():
    query = ''' \
            select distinct [Name],email 
            from SampleDataValidation 
            where email not like '%@%.com' 
          '''
    return query

def valid_DOB():
    query='''
        select distinct [Name],DateOfBirth from SampleDataValidation where DateOfBirth<=getdate()
    '''
    return query

def invalid_DOB():
    query='''
        with age_info as (
    select [Name],Email,Age,
    case when month(getdate())>month(DateofBirth)
      or (month(getdate())=month(DateofBirth) and day(getdate())>=day(DateofBirth))
     then datediff(year,DateOfBirth,getdate())
     else datediff(year,DateOfBirth,getdate()) -1
     end as cal_age from SampleDataValidation )
     select * from age_info where cal_age<>Age ;
    '''
    return query

