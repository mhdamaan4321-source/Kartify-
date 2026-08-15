from django.core.management.base import BaseCommand
from core.models import City

class Command(BaseCommand):
    help = 'Load Sri Lankan Cities into database'

    def handle(self, *args, **kwargs):
        cities = [
            "Colombo", "Dehiwala-Mount Lavinia", "Moratuwa", "Kotte", "Kaduwela", 
            "Maharagama", "Kesbewa", "Boralesgamuwa", "Kolonnawa", "Rajagiriya", "Battaramulla",
            "Gampaha", "Negombo", "Wattala", "Kelaniya", "Ja-Ela", "Katunayake", 
            "Minuwangoda", "Kadawatha", "Ragama",
            "Kalutara", "Panadura", "Beruwala", "Horana", "Mathugama", "Bandaragama",
            "Kandy", "Peradeniya", "Gampola", "Nawalapitiya", "Katugastota", "Akurana", "Kadugannawa",
            "Matale", "Dambulla", "Sigiriya", "Galewela", "Rattota",
            "Nuwara Eliya", "Hatton", "Talawakele", "Ginigathhena", "Ragala",
            "Galle", "Ambalangoda", "Hikkaduwa", "Elpitiya", "Baddegama",
            "Matara", "Weligama", "Dickwella", "Akuressa", "Kamburupitiya",
            "Hambantota", "Tangalle", "Tissamaharama", "Ambalantota", "Beliatta",
            "Kurunegala", "Kuliyapitiya", "Nikaweratiya", "Pannala", "Narammala",
            "Puttalam", "Chilaw", "Nattandiya", "Wennappuwa", "Marawila", "Kalpitiya",
            "Anuradhapura", "Eppawala", "Medawachchiya", "Kahatagasdigiliya",
            "Polonnaruwa", "Kaduruwela", "Hingurakgoda", "Medirigiriya",
            "Badulla", "Bandarawela", "Welimada", "Haputale", "Mahiyanganaya", "Diyatalawa",
            "Monaragala", "Wellawaya", "Bibile", "Kataragama", "Buttala",
            "Ratnapura", "Embilipitiya", "Pelmadulla", "Balangoda", "Eheliyagoda",
            "Kegalle", "Mawanella", "Warakapola", "Rambukkana", "Ruwanwella",
            "Jaffna", "Nallur", "Chavakachcheri", "Point Pedro", "Valvettithurai",
            "Kilinochchi", "Mannar", "Vavuniya", "Mullaitivu",
            "Trincomalee", "Kinniya", "Muttur", "Kantale",
            "Batticaloa", "Kattankudy", "Eravur", "Valaichchenai",
            "Ampara", "Kalmunai", "Sammanthurai", "Akkaraipattu", "Pottuvil"
        ]

        added_count = 0
        for city_name in cities:
            obj, created = City.objects.get_or_create(name=city_name)
            if created:
                added_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {added_count} new cities to the database!'))