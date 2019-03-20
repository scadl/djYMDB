'''
Adapter is a service script, containg several simple manipulations
able to adjust and database to fit old data from ymdb-1 and wp
'''
from ymdb.models import ArtObject, GenerTag

#for AO in ArtObject.objects.all().filter(InCollection=2):
for AO in ArtObject.objects.all():

    AID = AO.pk

    # Convert YMDB-1 Genres Array to actual GenresTAg
    '''SB = AO.ArtSubTitle.split('/')
    AO.ArtGeners.set(SB[:-1])'''

    # This will YMDB-1 convers Seasons and Episodes array into int constants
    '''SQ = 0
    SR = 0
    SB = AO.UserComment.split('/')[:-1]
    for SP in SB:
        SS = SP.split('!')
        SQ += 1
        SR += int(SS[1])

    AO.ArtBlocks = SQ
    AO.ArtParts = SR
    AO.save()'''

    #This will split YMDB-1 common namings to main and additional title
    '''SB = AO.ArtTitle.split('/')
    AO.ArtTitle = SB[-1]
    AO.ArtSubTitle = ''
    for s in SB[:-1]:
        AO.ArtSubTitle += '- '+s+'\n'
    AO.save()

    AO.UserComment = ''
    AO.save()'''

    # Little cached cover leanup
    if AO.ArtCoverCahed == 'no_cover.png':
        AO.ArtCoverCahed = ''
        AO.save()

    print( AID )


