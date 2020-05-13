from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers

from .models import ArtObject, Collections, GenerTag, sysSettings, guestTestimonilas
from .forms import ArtForm, CollectionForm, GenerTagForm, FormSettings, ExRegForm

# Create your views here.
def arts_list(req, gid=-1, cid=-1, pg=0, u=1):

    # If User already in system,
    # just rewrite from session
    if req.user.id:
        u = req.user.id

    try:
        # Try to load user settings
        uSettigs = sysSettings.objects.filter(theUser=u)[0]
    except LookupError:
        # No settings, create new object
        newSet = sysSettings(theUser = get_object_or_404(User, pk=u), pageStep = 6, navTheme = 'navbar-dark bg-dark')
        # Save this object to db
        newSet.save()
        # Load them as curent setings
        uSettigs = sysSettings.objects.filter(theUser=u)[0]

    # Preload settings object to a form
    setForm = FormSettings(instance=uSettigs)
    pageStep = uSettigs.pageStep
    uStyle = uSettigs.navTheme

    allCollect = Collections.objects.filter(theUser=u)
    req.session['uStyle'] = uStyle
    req.session['uPage'] = pg
    req.session['uGenre'] = gid
    req.session['uCollect'] = cid
    rkWord = ''

    if gid > -1:
        # Filter by genre
        allArts = ArtObject.objects.filter(ArtGeners=gid)[(pg*pageStep):(pageStep+(pg*pageStep))]
        nfArts = ArtObject.objects.filter(ArtGeners=gid)
    elif cid > -1:
        # Filter by collection
        allArts = ArtObject.objects.filter(InCollection=cid)[(pg*pageStep):(pageStep+(pg*pageStep))]
        nfArts = ArtObject.objects.filter(InCollection=cid)
    elif req.method == 'POST':
        # Search by keyword
        allArts = ArtObject.objects.filter(
            Q(ArtTitle__contains=req.POST.get('kw', None)) | Q(ArtSubTitle__contains=req.POST.get('kw', None)), theUser=u
        )[(pg * pageStep):(pageStep + (pg * pageStep))]
        nfArts = ArtObject.objects.filter(
            Q(ArtTitle__contains=req.POST.get('kw', None))|Q(ArtSubTitle__contains=req.POST.get('kw', None)), theUser=u
        )
        rkWord = req.POST.get('kw', None);
    else:
        # Just show the fist page with offcet
        allArts = ArtObject.objects.filter(theUser=u)[(pg*pageStep):(pageStep+(pg*pageStep))]
        nfArts = ArtObject.objects.filter(theUser=u)

    #print(pageStep, ':',  pg*pageStep)
    #print(req.POST.get('kw', None))

    VContext = {'artsList': allArts,
                'collsList': allCollect,
                'pages':range(0, nfArts.count()//pageStep+1),
                'uStyle': req.session['uStyle'],
                'active': req.session['uPage'],
                'gid': req.session['uGenre'],
                'cid': req.session['uCollect'],
                'uk': u,
                'kWord': rkWord,
                'sForm' : setForm}

    return render(req, 'artList.html', VContext)

@login_required
def art_add(req, refF=-1):

    # Getting some kind of data-caring request
    if req.method == 'POST':

        # Set the fake form value for model
        #req.POST = req.POST.copy()
        #req.POST['theUser'] = req.user.id

        # Create a Model Form instance from POST data,
        # populate it with data from request.
        myForm = ArtForm(data = req.POST, files=req.FILES)

        if myForm.is_valid():
            # Form is valid, so we can try to save it to DB

            # Create, but don't save the new object instance.
            thisArt = myForm.save(commit=False)
            # Mendel with new object properties: User should be an object too.
            thisArt.theUser = get_object_or_404(User, pk=req.user.id)

            # Display object contents (print_v)
            #print(thisArt.__dict__)

            # Save the new instance.
            thisArt.save()

            # Now, save the many-to-many data for the form.
            myForm.save_m2m()

            if refF == 1:
                return redirect('genFilter', gid=req.session['uGenre'], pg=req.session['uPage'])
            elif refF == 2:
                return redirect('collFilter', cid=req.session['uCollect'], pg=req.session['uPage'])
            else:
                return redirect('pageU', pg=req.session['uPage'])
    else:
        # Not a data-caring request:
        myForm = ArtForm() # provide empty form
        # Filter "tags" form element by current user id, avoiding mixing in artObject props
        myForm.fields['ArtGeners'].queryset = GenerTag.objects.filter(theUser=req.user.pk)
        myForm.fields['InCollection'].queryset = Collections.objects.filter(theUser=req.user.pk)

    VContext = {'formData':myForm,
                'formMode':True,
                'uStyle': req.session['uStyle'],
                'refFS':refF}
    return render(req, 'artForm.html', VContext)

@login_required
def art_edit(req, pk, refF=-1, rtg=-1, rpg=0):
    thisArt = get_object_or_404(ArtObject, pk=pk)
    if req.method == 'POST':
        myForm = ArtForm(instance=thisArt, data=req.POST, files=req.FILES)
        if myForm.is_valid():
            myForm.save()
            if refF == 1:
                return redirect('genFilter', gid=rtg, pg=rpg)
            elif refF == 2:
                return redirect('collFilter', cid=rtg, pg=rpg)
            else:
                return redirect('pageU', pg=rpg)
    else:
        myForm = ArtForm(instance=thisArt)
        myForm.fields['ArtGeners'].queryset = GenerTag.objects.filter(theUser=req.user.pk)

    VContext = {'formData':myForm, 'formMode':False,
                'refFS':refF, 'rtgS':rtg, 'rpgS':rpg,
                'uStyle': req.session['uStyle'],}
    return render(req, 'artForm.html', VContext)

@login_required()
def prop_edit(req, ref, pky=-1):
    if ref == 1:
        if pky == -1:
            if req.method == 'POST':
                cForm = CollectionForm(data=req.POST)
            else:
                cForm = CollectionForm
        else:
            if req.method == 'POST':
                cForm = CollectionForm(instance=Collections.objects.get(pk=pky), data=req.POST)
            else:
                cForm = CollectionForm(instance=Collections.objects.get(pk=pky))
        allColl = Collections.objects.filter(theUser=req.user.id)
        isCol = True

    if ref == 2:
        if pky == -1:
            if req.method == 'POST':
                cForm = GenerTagForm(data=req.POST)
            else:
                cForm = GenerTagForm
        else:
            if req.method == 'POST':
                cForm = GenerTagForm(instance=GenerTag.objects.get(pk=pky), data=req.POST)
            else:
                cForm = GenerTagForm(instance=GenerTag.objects.get(pk=pky))
        allColl = GenerTag.objects.filter(theUser=req.user.id)
        isCol = False

    if req.method == 'POST':
        if cForm.is_valid():
            thisCol = cForm.save(commit=False)
            thisCol.theUser = get_object_or_404(User, pk=req.user.id)
            thisCol.save()
            cForm.save_m2m()
            return redirect('propEdit', ref=ref)

    VContext = {'theForm':cForm, 'AllList':allColl,
                'isColl':isCol, 'delAct': ref,
                'uStyle': req.session['uStyle']}
    return render(req, 'collList.html', VContext)


@login_required()
def delSomething(req, pk, ref, refF=-1, rtg=-1, rpg=0):
    if ref == 0:
        """ This is request from card (bookmark) """
        refData = ArtObject.objects.get(pk=pk)
    if ref == 1:
        """ This is request from collections """
        refData = Collections.objects.get(pk=pk)
        refRedir = 1
    if ref == 2:
        """ This is request from genres """
        refData = GenerTag.objects.get(pk=pk)
        refRedir = 2
    refData.delete()
    if ref == 0:
        if refF == 1:
            return redirect('genFilter', gid=rtg, pg=rpg)
        elif refF == 2:
            return redirect('collFilter', cid=rtg, pg=rpg)
        else:
            return redirect('pageU', pg=rpg)

    else:
        return redirect('propEdit', ref=refRedir)

@login_required
def chpass (req):
    usr = get_object_or_404(User, pk=req.user.id)
    usr.set_password(req.GET.get('upass', None))
    usr.save()

    data = {'vars':0}
    return JsonResponse(data)

@login_required
def chSettings(req):

    uSettings = get_object_or_404(sysSettings, theUser=req.user.pk)
    uSetForm = FormSettings(instance=uSettings, data=req.POST)
    if uSetForm.is_valid:
        uSetForm.theUser = get_object_or_404(User, pk=req.user.id)
        uSetForm.save()
        return redirect('ArtList')

def sendTs(req):
    aTg = ArtObject.objects.get(pk=req.GET.get('aIdent', int))
    newTs = guestTestimonilas.objects.create(ArtBind=aTg)
    newTs.tsName = req.GET.get('gName', None)
    newTs.tsText = req.GET.get('gText', None)
    if req.GET.get('uName', None) != '':
        newTs.isAdmin = 1
    newTs.save()

    data = {'vars': 0}
    return JsonResponse(data)

def delTS(req):
    tsWork = guestTestimonilas.objects.get(pk=req.GET.get('aIdent', int))
    tsWork.delete()

    data = {'vars': 0}
    return JsonResponse(data)

def dynaTSLoad(req):
    tsList = guestTestimonilas.objects.filter(ArtBind=req.GET.get('aIdent', int))
    tsData = serializers.serialize('json', tsList)
    return JsonResponse(tsData, content_type='application/json', safe=False)

def getArtInfo(req, pk, u):
    artData = thisArt = get_object_or_404(ArtObject, pk=pk)
    return render(req, 'artPage.html', {'sArt':artData, 'shareUri':req.build_absolute_uri(), 'uk': u});

def registerNew(req):
    if req.method == 'POST':
        myForm = ExRegForm(req.POST)
        if myForm.is_valid():
            myForm.save()
            username = myForm.cleaned_data.get('username')
            raw_password = myForm.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return redirect('ArtList', u=user.id)
    else:
        myForm = ExRegForm()

    return render(req, 'registration/login.html', {'form': myForm, 'regMode': True})
