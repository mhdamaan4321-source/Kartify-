import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kartify_project.settings')
django.setup()

from core.models import Province, District, City

def load_data():
    locations_data = {
        "Western Province": {
            "Colombo": ["Colombo", "Dehiwala-Mount Lavinia", "Moratuwa", "Sri Jayawardenepura Kotte", "Negombo (Sub)", "Maharagama", "Kottawa", "Homagama", "Kaduwela", "Kolonnawa", "Battaramulla", "Piliyandala"],
            "Gampaha": ["Gampaha", "Negombo", "Ja-Ela", "Wattala", "Kelaniya", "Kadawatha", "Minuwangoda", "Divulapitiya", "Mirigama", "Kiribathgoda"],
            "Kalutara": ["Kalutara", "Panadura", "Beruwala", "Aluthgama", "Mathugama", "Horana", "Bandaragama"]
        },
        "North Western Province (Wayamba)": {
            "Puttalam": ["Puttalam", "Chilaw (Halawatha)", "Wennappuwa", "Nattandiya", "Marawila", "Madampe", "Anamaduwa", "Kalpitiya", "Dankotuwa"],
            "Kurunegala": ["Kurunegala", "Kuliyapitiya", "Narammala", "Pannala", "Nikaweratiya", "Polgahawela", "Hettipola", "Galgamuwa"]
        },
        "Central Province": {
            "Kandy": ["Kandy", "Peradeniya", "Katugastota", "Gampola", "Nawalapitiya", "Akurana", "Kadugannawa", "Wattegama"],
            "Matale": ["Matale", "Dambulla", "Sigiriya", "Galewela", "Rattota"],
            "Nuwara Eliya": ["Nuwara Eliya", "Hatton", "Talawakele", "Ginigathena", "Maskeliya", "Ragala"]
        },
        "Southern Province": {
            "Galle": ["Galle", "Ambalangoda", "Elpitiya", "Hikkaduwa", "Baddegama", "Bentota"],
            "Matara": ["Matara", "Weligama", "Dikwella", "Akuressa", "Kamburupitiya"],
            "Hambantota": ["Hambantota", "Tangalle", "Tissamaharama", "Ambalantota", "Beliatta"]
        },
        "Northern Province": {
            "Jaffna": ["Jaffna", "Nallur", "Chavakachcheri", "Point Pedro", "Valvettithurai", "Kankesanthurai"],
            "Mannar": ["Mannar", "Pesalai", "Nanaddan"],
            "Vavuniya": ["Vavuniya", "Cheddikulam"],
            "Mullaitivu": ["Mullaitivu", "Puthukkudiyiruppu", "Oddusuddan"],
            "Kilinochchi": ["Kilinochchi", "Paranthan", "Pallai"]
        },
        "Eastern Province": {
            "Batticaloa": ["Batticaloa", "Kattankudy", "Eravur", "Valaichchenai", "Kiran"],
            "Trincomalee": ["Trincomalee", "Kinniya", "Muttur", "Kantale"],
            "Ampara": ["Ampara", "Kalmunai", "Sammanthurai", "Akkaraipattu", "Pottuvil", "Uhana"]
        },
        "Uva Province": {
            "Badulla": ["Badulla", "Bandarawela", "Welimada", "Diyatalawa", "Mahiyanganaya", "Hali-Ela"],
            "Monaragala": ["Monaragala", "Wellawaya", "Bibile", "Kataragama", "Buttala"]
        },
        "Sabaragamuwa Province": {
            "Ratnapura": ["Ratnapura", "Embilipitiya", "Pelmadulla", "Balangoda", "Kuruwita", "Eheliyagoda"],
            "Kegalle": ["Kegalle", "Warakapola", "Mawanella", "Rambukkana", "Ruwanwella", "Yatiyanthota"]
        },
        "North Central Province": {
            "Anuradhapura": ["Anuradhapura", "Kekirawa", "Medawachchiya", "Tambuttegama", "Eppawala", "Habarana"],
            "Polonnaruwa": ["Polonnaruwa", "Kaduruwela", "Hingurakgoda", "Medirigiriya", "Welikanda"]
        }
    }

    for prov_name, districts in locations_data.items():
        prov_obj, _ = Province.objects.get_or_create(name=prov_name)
        for dist_name, cities in districts.items():
            dist_obj, _ = District.objects.get_or_create(name=dist_name, province=prov_obj)
            for city_name in cities:
                City.objects.get_or_create(name=city_name, district=dist_obj)

    print("Successfully loaded all Sri Lankan Provinces, Districts, and Cities!")

if __name__ == '__main__':
    load_data()