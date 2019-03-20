from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from .models import ArtObject, Collections, GenerTag, sysSettings
from .forms import ArtForm, CollectionForm, GenerTagForm, FormSettings

# Create your views here.
def arts_list(req, gid=-1, cid=-1, pg=0):

    try:
        uSettigs = sysSettings.objects.all()[0]
    except LookupError:
        newSet = sysSettings(theUser = User.objects.all[0], pageStep = 6, navTheme = 'navbar-dark bg-dark')
        newSet.save()
        uSettigs = sysSettings.objects.all()[0]

    setForm = FormSettings(instance=uSettigs)
    pageStep = uSettigs.pageStep
    uStyle = uSettigs.navTheme

    allCollect = Collections.objects.all()
    req.session['uStyle'] = uStyle
    req.session['uPage'] = pg
    req.session['uGenre'] = gid
    req.session['uCollect'] = cid
    rkWord = ''

    if gid > -1:
        allArts = ArtObject.objects.filter(ArtGeners=gid)[(pg*pageStep):(pageStep+(pg*pageStep))]
        nfArts = ArtObject.objects.filter(ArtGeners=gid)
    elif cid > -1:
        allArts = ArtObject.objects.filter(InCollection=cid)[(pg*pageStep):(pageStep+(pg*pageStep))]
        nfArts = ArtObject.objects.filter(InCollection=cid)
    elif req.method == 'POST':
        allArts = ArtObject.objects.filter(
            Q(ArtTitle__contains=req.POST.get('kw', None)) | Q(ArtSubTitle__contains=req.POST.get('kw', None))
        )[(pg * pageStep):(pageStep + (pg * pageStep))]
        nfArts = ArtObject.objects.filter(
            Q(ArtTitle__contains=req.POST.get('kw', None))|Q(ArtSubTitle__contains=req.POST.get('kw', None))
        )
        rkWord = req.POST.get('kw', None);
    else:
        allArts = ArtObject.objects.all()[(pg*pageStep):(pageStep+(pg*pageStep))]
        nfArts = ArtObject.objects.all()

    #print(pageStep, ':',  pg*pageStep)
    print(req.POST.get('kw', None))

    VContext = {'artsList': allArts,
                'collsList': allCollect,
                'pages':range(0, nfArts.count()//pageStep+1),
                'uStyle': req.session['uStyle'],
                'active': req.session['uPage'],
                'gid': req.session['uGenre'],
                'cid': req.session['uCollect'],
                'kWord': rkWord,
                'sForm' : setForm}

    return render(req, 'artList.html', VContext)

@login_required
def art_add(req, refF=-1):
    if req.method == 'POST':
        myForm = ArtForm(data = req.POST, files=req.FILES)
        if myForm.is_valid():
            thisArt = myForm.save(commit=False)
            thisArt.save()
            myForm.save_m2m()
            if refF == 1:
                return redirect('genFilter', gid=req.session['uGenre'], pg=req.session['uPage'])
            elif refF == 2:
                return redirect('collFilter', cid=req.session['uCollect'], pg=req.session['uPage'])
            else:
                return redirect('pageU', pg=req.session['uPage'])
    else:
        myForm = ArtForm
        #myForm.fields['ArtSubTitle'].widget.attrs = {'style':'height:110px'}
        #myForm.fields['ArtGeners'].widget.attrs = {'style':'height:295px'}
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
        #myForm.fields['ArtSubTitle'].widget.attrs = {'style':'height:110px'}
        #myForm.fields['ArtGeners'].widget.attrs = {'style':'height:295px'}
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
        allColl = Collections.objects.all()
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
        allColl = GenerTag.objects.all()
        isCol = False

    if req.method == 'POST':
        if cForm.is_valid():
            thisCol = cForm.save(commit=False)
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
    usr = User.objects.get(username=req.GET.get('uname', None))
    usr.set_password(req.GET.get('upass', None))
    usr.save()

    data = {'vars':0}
    return JsonResponse(data)

def chSettings(req):

    uSettings = get_object_or_404(sysSettings, theUser=req.user.pk)
    uSetForm = FormSettings(instance=uSettings, data=req.POST)
    if uSetForm.is_valid:
        uSetForm.save()
        return redirect('ArtList')

