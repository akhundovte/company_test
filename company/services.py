from .models import CompanyUserIx, Company, News


def has_bind_user_to_company(user, company):
    return CompanyUserIx.objects.filter(company=company, user=user).exists()


def create_bind_user_to_company(user_id, company_id):
    return CompanyUserIx.objects.create(company_id=company_id, user_id=user_id)


def get_all_companies():
    return Company.objects.all()


def get_company_by_id(company_id):
    try:
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist:
        raise EntityDoesNotExist
    return company


def get_news_with_company_by_id(news_id):
    try:
        news = News.objects.select_related('company').get(pk=news_id)
    except News.DoesNotExist:
        raise EntityDoesNotExist
    return news


class EntityDoesNotExist(Exception):
    pass
