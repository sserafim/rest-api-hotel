from sql_alchemy import banco


# Cria um objeto model da clase HotelModel
class SiteModel(banco.Model):

    __tablename__ = 'sites'

    site_id = banco.Column(banco.integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    # Cria os campos do modelo da classe hotel >>Isso é um objeto<<
    def __init__(self, url):
        self.url = url

    # Funcão que Transforma um objeto em um fomato DICIONÁRIO que converte/ou é um JSON - automaticamente >>>  <<<

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        url = cls.query.filter_by(url=url).first()
        if url:
            return url
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def update_site(self, url):
        self.url = url

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()
