from urllib import response
from xmlrpc.client import DateTime
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import select_template
from decimal import Decimal
import datetime
from django.core.exceptions import ValidationError
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from tablib import Dataset
from import_export import resources
import operator
from django.db.models.signals import post_save
from django.contrib.admin.views.decorators import staff_member_required

from employeeApp.models import employeePersonalDetails
from productPagesApp.models import seedFundingContactUsSignup, growthFundingContactUsSignup, \
    earlyFundingContactUsSignup, privateBoutiqueContactUs, sellESOPContactUs, sellYourStartupContactUs
from stockApp.resources import *
from .forms import *
from .models import *
from babel.numbers import format_currency
from newsBlogApp.models import blogNews
from videoShortsApp.models import blogVideosShorts
from videoBlogApp.models import blogVideos
from articleBlogApp.models import blogArticles
from websiteApp.models import buyPreIPOStockList
from django.db import connections
from .peersCrawl import crawlScreenerView, getScreenerPriceForStock, crawlScreenerForBankNBFCView, numberConversion
from django.http import HttpResponseRedirect
from brokenRedirectApp.models import redirectBucket, redirectCount
from staticPagesSlugApp.models import staticPagesSlugs
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
import json
from json import JSONEncoder
import decimal
from rest_framework import status
import os
import aspose.slides as slides
import aspose.pydrawing as drawing
import requests
import shutil
import base64
from django.db.models import Q
from authApp.models import UserAdvisors

from authApp.services.dashboard_service import DashboardService
from productPagesApp.serializers import seedFundingContactUsSignupSerializer, growthFundingContactUsSignupSerializer, \
    earlyFundingContactUsSignupSerializer, privateBoutiqueContactUsSerializer, sellESOPContactUsSerializer, \
    sellYourStartupContactUsSerializer

from authApp.serializers import UserAdvisorSerializer
#
currentYear = datetime.datetime.now().strftime("%Y")


def financialreportimageView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(annualReportsDHRPImage, pk=pkID)
        objForm = annualReportsDHRPImageForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'annualReportsDHRPImage sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def financialreportimageViewAPI(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)

    # POST API
    if request.method == 'POST':
        request.data['stockProfileName'] = stock.id
        annualReportsDHRPImage_serializer = annualReportsDHRPImageSerializer(data=request.data)
        if annualReportsDHRPImage_serializer.is_valid():
            annualReportsDHRPImage_serializer.save()
            response = annualReportsDHRPImage.objects.filter(stockProfileName_id=stock.id)
            serializer = annualReportsDHRPImageSerializer(response, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(annualReportsDHRPImage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET API
    if request.method == 'GET':
        id = request.data.get('id')
        if id:
            response = annualReportsDHRPImage.objects.filter(id=id).first()
            if response:
                serializer = annualReportsDHRPImageSerializer(response)
                return Response({"images": serializer.data})
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            response = annualReportsDHRPImage.objects.filter(stockProfileName_id=stock.id)
            serializer = annualReportsDHRPImageSerializer(response, many=True)
            return Response(serializer.data)

    id = request.data.get('id')
    if request.method == 'DELETE':
        if id:
            response = annualReportsDHRPImage.objects.filter(id=id).first()
            if response:
                response.delete()
                return Response({
                    'msg': 'Data Deleted Successfully'
                })
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'id Field is Required'
            })
    if request.method == 'PUT':
        if id:
            response = annualReportsDHRPImage.objects.filter(id=id).first()
            if response:
                request.data['stockProfileName'] = stock.id
                serializer = annualReportsDHRPImageSerializer(response, data=request.data)
                serializer_checker = serializer_valid(serializer)
                return Response(serializer_checker)
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'Id Filed Required'
            })


@api_view(['GET'])
def commonapiViewAPI(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        try:
            stock_serializer = StockSerializer(stock)
            show_on_pitch = stock_serializer.data.get("showOnPitchPage")
            stock_name = stock_serializer.data.get("stockName")
            heading = stock_serializer.data.get("headingForStartup")
            type_Of_Shares = stock_serializer.data.get("type_Of_Shares")
            shareDematerialized = stock_serializer.data.get("shareDematerialized")
            amount_To_Raise = stock_serializer.data.get("amount_To_Raise")
            daysLeft = stock_serializer.data.get("daysLeft")
            investment_Raised = stock_serializer.data.get("investment_Raised")
            jump_Start_raised_from_investor = stock_serializer.data.get("jump_Start")
            min_invest = stock_serializer.data.get("min_invest")
            launch_date = stock.days_left
            active_campaigns = campaign.objects.filter(stockProfileName=slug, isActive=True)

        except:
            stock_name = None
            heading = None
            type_Of_Shares = None
            shareDematerialized = None
            amount_To_Raise = None
            daysLeft = None
            investment_Raised = None
            jump_Start_raised_from_investor = None
            min_invest = None
            launch_date = None
            active_campaigns = None

        type_of_company = None
        equityPercent = None
        investorPrice = None
        try:
            essentialInst = stockEssentials.objects.filter(stockProfileName=slug)
            for each in essentialInst:
                type_of_company = each.typeOfCompany.name
                equityPercent = each.equityPercent
        except:
            type_of_company = None
            equityPercent = None

        try:
            response = annualReportsDHRPImage.objects.filter(stockProfileName_id=stock.id)
            serializer = annualReportsDHRPImageSerializer(response, many=True)
            financial_report_image = serializer.data
        except:
            financial_report_image = None

        try:
            buypreipoInst = buyPreIPOStockList.objects.filter(stockName=slug)
            for each in buypreipoInst:
                investorPrice = each.investorPrice
        except:
            investorPrice = None

        newsVideoshead_list = []
        try:
            newsVideos = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
                '-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideoshead_list.append(newsVideos_serial.data)
        except:
            newsVideoshead_list = []
        
        active_campaigns_list = []
        if len(active_campaigns):
            for each in active_campaigns:
                active_campaigns_list.append(campaignSerializer(each).data)

        context = {
            "stock_name": stock_name,
            "show_on_pitch": show_on_pitch,
            "stock_heading": heading,
            "type_Of_Shares": type_Of_Shares,
            "shareDematerialized": shareDematerialized,
            "type_of_company": type_of_company,
            "financial_report_image": financial_report_image,
            "amount_To_Raise": amount_To_Raise,
            "daysLeft": daysLeft,
            "investment_Raised": investment_Raised,
            "jump_Start_raised_from_investor": jump_Start_raised_from_investor,
            "min_invest": min_invest,
            "launch_date": launch_date,
            "equityPercent": equityPercent,
            "investorPrice": investorPrice,
            "newsVideoshead_list": newsVideoshead_list,
            "active_campaigns": active_campaigns_list
        }
        return Response(context)


def pitchView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    # print(stock.id)
    # print(stock, "$$$$$$$$$$$$$$$$$$$$$$$$")

    # HIGHLIGHTS
    try:
        highLightsInst = highLights.objects.filter(stockProfileName_id=stock.id)
        highlights_serializer = highLightsSerializer(highLightsInst, many=True)
        highlights_data = highlights_serializer.data
        highlights_data = json.dumps(highlights_data)
        highlights_data_serialized_data = json.loads(highlights_data)
    except:
        highLightsInst = None
        highlights_data_serialized_data = None

    highLightsInstcreate = None
    try:
        highLightsInstcreate = highLights.objects.get(stockProfileName_id=stock.id)
    except:
        highLightsInstcreate = None

    createhighlights = highLightsForm(instance=highLightsInstcreate)

    # INVESTMENT CHECKLIST
    try:
        stockInvestmentChecklistInst = stockInvestmentChecklist.objects.get(stockProfileName_id=stock.id)
        management = str(stockInvestmentChecklistInst.management)
        acountingPratice = str(stockInvestmentChecklistInst.acountingPratice)
        profitability = str(stockInvestmentChecklistInst.profitability)
        solvency = str(stockInvestmentChecklistInst.solvency)
        growth = str(stockInvestmentChecklistInst.growth)
        valuation = str(stockInvestmentChecklistInst.valuation)
    except:
        stockInvestmentChecklistInst = None
        management = None
        acountingPratice = None
        profitability = None
        solvency = None
        growth = None
        valuation = None

    stockInvestmentChecklistInstcreate = None
    try:
        stockInvestmentChecklistInstcreate = stockInvestmentChecklist.objects.get(stockProfileName_id=stock.id)
    except:
        stockInvestmentChecklistInstcreate = None

    createstockInvestmentChecklist = stockInvestmentChecklistForm(instance=stockInvestmentChecklistInstcreate)

    # STOCKOWNERSHIP
    try:
        stockOwnershipInst = stockOwnership.objects.get(stockProfileName_id=stock.id)
    except:
        stockOwnershipInst = None

    try:
        stockOwnershipDirectorInst = stockOwnershipDirector.objects.filter(stockProfileName_id=stock.id)
        stockOwnershipDirector_serializer = stockOwnershipDirectorSerializer(stockOwnershipDirectorInst, many=True)
        stockOwnershipDirector_data = stockOwnershipDirector_serializer.data
        stockOwnershipDirector_data = json.dumps(stockOwnershipDirector_data)
        stockOwnershipDirector_serialized_data = json.loads(stockOwnershipDirector_data)
    except:
        stockOwnershipDirectorInst = None
        stockOwnershipDirector_serialized_data = None

    try:
        stockOwnershipDirectorInstcreate = stockOwnershipDirector.objects.get(stockProfileName_id=stock.id)
    except:
        stockOwnershipDirectorInstcreate = None

    createstockOwnershipDirector = stockOwnershipDirectorForm(instance=stockOwnershipDirectorInstcreate)

    # DECK
    try:
        deckInst = deck.objects.filter(stockProfileName_id=stock.id).last()
        # print(deckInst, "$$$$$$$$$$$$$$$$$$$")
    except:
        deckInst = None

    try:
        deckInstcreate = deck.objects.get(stockProfileName_id=stock.id)
    except:
        deckInstcreate = None

    createdeck = deckForm(instance=deckInstcreate)

    # DECKIMAGES
    try:
        deck_imagesInst = deck_images.objects.filter(deckname_id=deckInst.id)
        deck_images_serializer = deck_imagesSerializer(deck_imagesInst, many=True)
        deck_images_data = deck_images_serializer.data
        deck_images_data = json.dumps(deck_images_data)
        deck_images_data_serialized_data = json.loads(deck_images_data)
    except:
        deck_imagesInst = None
        deck_images_data_serialized_data = None
    try:
        deck_imagesInstcreate = deck_images.objects.get(deckname_id=deckInst.id)
    except:
        deck_imagesInstcreate = None
    createdeck_images = deck_imagesForm(instance=deck_imagesInstcreate)

    # NEWSVIDEOS
    try:
        newsVideosInst = blogVideos.objects.filter(showinpitch=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosInst = None
    try:
        newsVideoshead = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideoshead = []

    # FINANCIAL IMAGE
    try:
        annualReportsDHRPImageInst = annualReportsDHRPImage.objects.filter(stockProfileName_id=stock.id)
        serializer = annualReportsDHRPImageSerializer(annualReportsDHRPImageInst, many=True)
        annualReportsDHRPImage_data = serializer.data
        annualReportsDHRPImage_data = json.dumps(annualReportsDHRPImage_data)
        report_image_serialized_data = json.loads(annualReportsDHRPImage_data)
    except:
        annualReportsDHRPImageInst = None
        report_image_serialized_data = None

    try:
        annualReportsDHRPImageInstcreate = annualReportsDHRPImage.objects.get(stockProfileName_id=stock.id)
    except:
        annualReportsDHRPImageInstcreate = None

    createannualReportsDHRPImageInst = annualReportsDHRPImageForm(instance=annualReportsDHRPImageInstcreate)

    # STOCK DATA
    try:
        stock_serializer = StockSerializer(stock)
        heading = stock_serializer.data.get("headingForStartup")
        type_Of_Shares = stock_serializer.data.get("type_Of_Shares")
        shareDematerialized = stock_serializer.data.get("shareDematerialized")
        amount_To_Raise = stock_serializer.data.get("amount_To_Raise")
        daysLeft = stock_serializer.data.get("daysLeft")
        investment_Raised = stock_serializer.data.get("investment_Raised")
        jump_Start_raised_from_investor = stock_serializer.data.get("jump_Start")
        min_invest = stock_serializer.data.get("min_invest")
        launch_date = stock.days_left

    except:
        heading = None
        type_Of_Shares = None
        shareDematerialized = None
        amount_To_Raise = None
        daysLeft = None
        investment_Raised = None
        jump_Start_raised_from_investor = None
        min_invest = None
        launch_date = None

    type_of_company = None
    equityPercent = None
    investorPrice = None
    try:
        essentialInst = stockEssentials.objects.filter(stockProfileName=slug)
        for each in essentialInst:
            type_of_company = each.typeOfCompany.name
            equityPercent = each.equityPercent
    except:
        type_of_company = None

    # STOCK PRICE
    try:
        buypreipoInst = buyPreIPOStockList.objects.filter(stockName=slug)
        for each in buypreipoInst:
            investorPrice = each.investorPrice
    except:
        investorPrice = None

    context = {
        "stock": stock,
        # 'annualReportsDHRPImageforpitch': annualReportsDHRPImageforpitch,
        "highlights": highlights_data_serialized_data,
        "createhighlights": createhighlights,
        "heading": heading,
        "type_Of_Shares": type_Of_Shares,
        "shareDematerialized": shareDematerialized,
        "type_of_company": type_of_company,
        "stockInvestmentChecklist": stockInvestmentChecklistInst,
        "createstockInvestmentChecklist": createstockInvestmentChecklist,
        "management": management,
        "acountingPratice": acountingPratice,
        "profitability": profitability,
        "solvency": solvency,
        "growth": growth,
        "valuation": valuation,
        "stockOwnershipDirector": stockOwnershipDirector_serialized_data,
        "createstockOwnershipDirector": createstockOwnershipDirector,
        "deck": deckInst,
        "createdeck": createdeck,
        "deck_images": deck_images_data_serialized_data,
        "createdeck_images": createdeck_images,
        "newsVideos": newsVideosInst,
        "newsVideoshead": newsVideoshead,
        "annualReportsDHRPImage": report_image_serialized_data,
        "createannualReportsDHRPImageInst": createannualReportsDHRPImageInst,
        "amount_To_Raise": amount_To_Raise,
        "daysLeft": daysLeft,
        "investment_Raised": investment_Raised,
        "min_invest": min_invest,
        "launch_date": launch_date,
        "equityPercent": equityPercent,
        "jump_Start_raised_from_investor": jump_Start_raised_from_investor,
        "investorPrice": investorPrice
    }
    return render(request, 'UI/pitch.html', context)


@api_view(['GET'])
def pitchViewAPI(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        try:
            highLights_data = highLights.objects.filter(stockProfileName_id=stock.id)
            highLights_serializer = highLightsSerializer(highLights_data, many=True)
            highlights_data = highLights_serializer.data
        except:
            highlights_data = None
        try:
            stockInvestmentChecklist_response = stockInvestmentChecklist.objects.filter(stockProfileName_id=stock.id)
            stockInvestmentChecklist_serializer = stockInvestmentChecklistSerializer(stockInvestmentChecklist_response,
                                                                                     many=True)
            stockInvestmentChecklist_data = stockInvestmentChecklist_serializer.data
        except:
            stockInvestmentChecklist_data = None

        try:
            stockOwnershipDirector_response = stockOwnershipDirector.objects.filter(stockProfileName_id=stock.id)
            stockOwnershipDirector_serializer = stockOwnershipDirectorSerializer(stockOwnershipDirector_response,
                                                                                 many=True)
            stockOwnershipDirector_data = stockOwnershipDirector_serializer.data
        except:
            stockOwnershipDirector_data = None

        try:
            ownershipInstitutionalInst = stockOwnershipInstitutional.objects.filter(stockProfileName=stock)
            if ownershipInstitutionalInst:
                investors_list = stockOwnershipInstitutionalSerializer(ownershipInstitutionalInst, many=True).data
        except:
            investors_list = []

        try:
            deck_response = deck.objects.filter(stockProfileName_id=stock.id)
            deck_serializer = deckSerializer(deck_response, many=True)
            deck_data = deck_serializer.data
        except:
            deck_data = None

        try:
            deck_response = deck_images.objects.filter(deckname__stockProfileName=stock.id)
            deckimages_serializer = deck_imagesSerializer(deck_response, many=True)
            deckimages_data = deckimages_serializer.data
        except:
            deckimages_data = None

        newsVideospitch_list = []
        try:
            newsVideos = blogVideos.objects.filter(showinpitch=True, relatedResearchReports=stock.id).order_by(
                '-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    each.videoLink = "http://youtu.be/"+ each.videoLink if each.videoLink else None
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideospitch_list.append(newsVideos_serial.data)
        except:
            newsVideospitch_list = []

        try:
            pitchDocs_response = pitchDocs.objects.filter(stockProfileName_id=stock.id)
            pitchDocs_serializer = pitchDocsSerializer(pitchDocs_response, many=True)
            pitchDocs_data = pitchDocs_serializer.data
        except:
            pitchDocs_data = None

        try:
            pitchDocsImages_response = pitchDocs_images.objects.filter(docname__stockProfileName=stock.id)
            pitchDocsImages_serializer = pitchDocs_imagesSerializer(pitchDocsImages_response, many=True)
            pitchDocsImages_data = pitchDocsImages_serializer.data
        except:
            pitchDocsImages_data = None

        

        null = None
        true = True
        false = False
        
        response_dict = {}
        stock_detail = {}
        stock_detail['extraData'] = {'seoTitle': stock.seoTitle, 'stockName': stock.stockName}
        stock_detail['highlights'] = {'label': 'Highlights', 'data': {}, 'child': {}}
        if highlights_data and highlights_data != []:
            stock_detail['highlights']['data'] = highlights_data

        if stock_detail['highlights']['data'] == [] and stock_detail['highlights']['child'] == {}:
            stock_detail.pop('highlights')

        stockInvestmentChecklist_data[0]['recommendation'] = get_object_or_404(recommendationOptions,
                                                                               id=stockInvestmentChecklist_data[0][
                                                                                   'recommendation']).name
        stockInvestmentChecklist_data[0]['businessType'] = get_object_or_404(businessTypeOptions,
                                                                             id=stockInvestmentChecklist_data[0][
                                                                                 'businessType']).name
        stock_detail['stockInvestmentChecklist'] = {'label': 'Business Rating', 'data': {}, 'child': {}}
        if stockInvestmentChecklist_data and stockInvestmentChecklist_data != []:
            stock_detail['stockInvestmentChecklist']['data'] = stockInvestmentChecklist_data

        if stock_detail['stockInvestmentChecklist']['data'] == {} and stock_detail['stockInvestmentChecklist'][
            'child'] == {}:
            stock_detail.pop('stockInvestmentChecklist')

        stock_detail['stockOwnershipDirector'] = {'label': 'Our Team', 'data': {}, 'child': {}}
        if stockOwnershipDirector_data and stockOwnershipDirector_data != []:
            stock_detail['stockOwnershipDirector']['data'] = stockOwnershipDirector_data

        if stock_detail['stockOwnershipDirector']['data'] == [] and stock_detail['stockOwnershipDirector'][
            'child'] == {}:
            stock_detail.pop('stockOwnershipDirector')

        stock_detail['newsVideospitch'] = {'label': 'Pitch', 'data': {}, 'child': {}}
        if newsVideospitch_list and newsVideospitch_list != []:
            stock_detail['newsVideospitch']['data'] = newsVideospitch_list

        if stock_detail['newsVideospitch']['data'] == [] and stock_detail['newsVideospitch']['child'] == {}:
            stock_detail.pop('newsVideospitch')

        stock_detail['investors'] = {'label': 'Investors', 'data': {}, 'child': {}}
        if investors_list and investors_list != []:
            stock_detail['investors']['data'] = investors_list
        
        if stock_detail['investors']['data'] == {} and stock_detail['investors']['child'] == {}:
            stock_detail.pop('investors')

        stock_detail['deck'] = {'label': 'Deck', 'data': {}, 'child': {}}   
        if deck_data and deck_data != []:
            stock_detail['deck']['data'] = deck_data
        if stock_detail['deck']['data'] == [] and stock_detail['deck']['child'] == {}:
            stock_detail.pop('deck')

        stock_detail['deck_images'] = {'label': 'Deck Images', 'data': {}, 'child': {}}
        if deckimages_data and deckimages_data != []:
            stock_detail['deck_images']['data'] = deckimages_data
        if stock_detail['deck_images']['data'] == [] and stock_detail['deck_images']['child'] == {}:
            stock_detail.pop('deck_images')

        stock_detail['pitchDocs'] = {'label': 'Pitch Docs', 'data': {}, 'child': {}}   
        if pitchDocs_data and pitchDocs_data != []:
            stock_detail['pitchDocs']['data'] = pitchDocs_data
        if stock_detail['pitchDocs']['data'] == [] and stock_detail['pitchDocs']['child'] == {}:
            stock_detail.pop('pitchDocs')

        stock_detail['pitchDocs_images'] = {'label': 'Pitch Docs Images', 'data': {}, 'child': {}}
        if pitchDocsImages_data and pitchDocsImages_data != []:
            stock_detail['pitchDocs_images']['data'] = pitchDocsImages_data
        if stock_detail['pitchDocs_images']['data'] == {} and stock_detail['pitchDocs_images']['child'] == {}:
            stock_detail.pop('pitchDocs_images')

        

        # response_dict.update({'stock': stock_detail})
        return Response(stock_detail)
    # return Response(context)
        #return Response(context)


def serializer_valid(serializer):
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return serializer.errors


def get_images_return(url):
    parent_dir = os.getcwd()

    print(parent_dir)
    img_directory = "deck_dir"
    path = os.path.join(parent_dir, img_directory)
    os.makedirs(path)
    try:
        response = requests.get(url)
        open("deck_dir/newdeck.pptx", "wb").write(response.content)

        # Load presentation
        pres = slides.Presentation("deck_dir/newdeck.pptx")

        for index in pres.slides:
            bmp = index.get_thumbnail(1, 1)
            os.chdir('{}/deck_dir'.format(parent_dir))
            bmp.save("Slide_{num}.jpg".format(num=str(index.slide_number)), drawing.imaging.ImageFormat.jpeg)

        res = []

        # Iterate directory
        for path in os.listdir('{}/deck_dir'.format(parent_dir)):
            # check if current path is a file
            if os.path.isfile(os.path.join('{}/deck_dir'.format(parent_dir), path)):
                res.append(path)
        print(res)
        new_res = []
        aa = '{}/deck_dir/'.format(parent_dir)
        for each_res in res:
            new_res.append(aa + each_res)
        for each_new_res in new_res:
            if "pptx" in each_new_res:
                new_res.remove(each_new_res)

        # print(new_res)

        ctx = {}
        for each in new_res:
            with open(each, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            ctx[each[-11:]] = image_data

        img_directory = "deck_dir"
        path = os.path.join(parent_dir, img_directory)
        os.chdir('{}'.format(parent_dir))
        shutil.rmtree(path)
        return ctx
    except:
        os.chdir('{}'.format(parent_dir))
        shutil.rmtree(path)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def deckimagesViewAPI(request, slug):
    deckinst = get_object_or_404(deck, id=slug)
    print(deckinst, "deckinstdeckinstdeckinstdeckinst")
    print(deckinst.id)

    if request.method == 'POST':
        request.POST._mutable = True
        request.data['deckname'] = deckinst.id
        deck_serializer = deck_imagesSerializer(data=request.data)
        if deck_serializer.is_valid():
            deck_serializer.save()
            response = deck_images.objects.filter(deckname=deckinst.id)
            serializer = deck_imagesSerializer(response, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(deck_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    id = deckinst.id
    if request.method == 'GET':
        if id:
            deck_image_response = deck_images.objects.filter(deckname=id)
            deck_images_response_Serializer = deck_imagesSerializer(deck_image_response, many=True)
            deck_images_data = deck_images_response_Serializer.data
            response = deck.objects.filter(id=id).first()
            if response:
                serializer = deckSerializer(response)
                aa = get_images_return(serializer.data.get("dec_ppt"))
                return Response({"deck_images_data": deck_images_data, "ppt_data": serializer.data, "images": aa})
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            response = deck_images.objects.all()
            serializer = deck_imagesSerializer(response, many=True)
            return Response(serializer.data)

    if request.method == 'PUT':
        if id:
            response = deck_images.objects.filter(id=id).first()
            if response:
                request.data['stockProfileName'] = deckinst.id
                serializer = deck_imagesSerializer(response, data=request.data)
                serializer_checker = serializer_valid(serializer)
                return Response(serializer_checker)
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'Id Filed Required'
            })

    if request.method == 'DELETE':
        if id:
            response = deck_images.objects.filter(id=id).first()
            if response:
                response.delete()
                return Response({
                    'msg': 'Data Deleted Successfully'
                })
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'id Field is Required'
            })


def deckimagesView(request):
    if request.method == 'POST':
        deckname = request.POST.get('deckname')
        stockInst = get_object_or_404(deck, pk=deckname)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = deck_images.objects.filter(deckname=deckname).last()
        objForm = deck_imagesForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'deck_images Type Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def upload_images(deck_url, deck_id, parent_dir, base_url):
    img_directory = "deck_dir"
    path = os.path.join(parent_dir, img_directory)
    os.makedirs(path)
    #print(path, "EEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    
    print(base_url)
    url = base_url+"/research-report/{}/deckimagesapi/".format(deck_id)
    response = requests.get(deck_url)
    open("{}/newdeck.pptx".format(path), "wb").write(response.content)

    # Load presentation
    pres = slides.Presentation("{}/newdeck.pptx".format(path))

    for index in pres.slides:
        bmp = index.get_thumbnail(1, 1)
        os.chdir('{}/deck_dir'.format(parent_dir))
        bmp.save("Slide_{num}.jpg".format(num=str(index.slide_number)), drawing.imaging.ImageFormat.jpeg)

    res = []

    # Iterate directory
    for path in os.listdir('{}/deck_dir'.format(parent_dir)):
        # check if current path is a file
        if os.path.isfile(os.path.join('{}/deck_dir'.format(parent_dir), path)):
            res.append(path)
    print(res)

    image_path_list = []
    aa = '{}/deck_dir/'.format(parent_dir)

    print(aa, "###########")
    for each_res in res:
        image_path_list.append(aa + each_res)
    for each_new_res in image_path_list:
        if "pptx" in each_new_res:
            image_path_list.remove(each_new_res)

    for each in image_path_list:
        payload = {'deckname': deck_id,
                   'page_description': 'Static Page Discription',
                   'tag': 'static tag'}
        files = [
            ('page_image', ('{}.jpg'.format(each[-11:]), open(each, 'rb'), 'image/jpeg'))
        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)
    img_directory = "deck_dir"
    path = os.path.join(parent_dir, img_directory)
    shutil.rmtree(path)


def update_image_of_deck(stockProfile, base_url):
    print(stockProfile, "&&&&&&&&&&&&&&&&&&&&")
    deckInst = deck.objects.filter(stockProfileName_id=stockProfile)
    print(deckInst, "%%%%%%%%%%%%%%%%%%%%")
    deck_serializer = deckSerializer(deckInst, many=True)
    data = deck_serializer.data
    deck_data = json.dumps(data)
    deck_serialized = json.loads(deck_data)
    deck_serialized = deck_serialized[-1]
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    parent_dir = os.getcwd()
    # for each in deck_serialized[-1]:
    print(deck_serialized, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    deck_id = deck_serialized["id"]
    deck_url = deck_serialized["dec_ppt"]
    upload_images(deck_url, deck_id, parent_dir, base_url)


def deckView(request):
    base_url = f"{ request.scheme }://{ request.get_host()}"
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(deck, pk=pkID)
        objForm = deckForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            update_image_of_deck(stockProfile, base_url)
            messages.success(request, 'Deck sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def deckViewAPI(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)

    if request.method == 'POST':
        request.POST._mutable = True
        request.data['stockProfileName'] = stock.id
        deck_serializer = deckSerializer(data=request.data)
        if deck_serializer.is_valid():
            deck_serializer.save()
            response = deck.objects.filter(stockProfileName_id=stock.id)
            serializer = deckSerializer(response, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(deck_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    id = request.data.get('id')
    if request.method == 'GET':
        if id:
            response = deck.objects.filter(id=id).first()
            if response:
                serializer = deckSerializer(response)
                aa = get_images_return(serializer.data.get("dec_ppt"))
                return Response({"ppt_data": serializer.data, "images": aa})
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            response = deck.objects.filter(stockProfileName_id=stock.id)
            serializer = deckSerializer(response, many=True)
            return Response(serializer.data)

    if request.method == 'DELETE':
        if id:
            response = deck.objects.filter(id=id).first()
            if response:
                response.delete()
                return Response({
                    'msg': 'Data Deleted Successfully'
                })
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'id Field is Required'
            })
    if request.method == 'PUT':
        if id:
            response = deck.objects.filter(id=id).first()
            if response:
                request.data['stockProfileName'] = stock.id
                serializer = deckSerializer(response, data=request.data)
                serializer_checker = serializer_valid(serializer)
                return Response(serializer_checker)
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'Id Filed Required'
            })


@api_view(['GET', 'POST'])
def stockOwnershipDirectorAPI(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    print(type(request.data))
    if request.method == 'GET':
        response = stockOwnershipDirector.objects.filter(stockProfileName_id=stock.id)
        if response.exists():
            serializer = stockOwnershipDirectorSerializer(response, many=True)
            return Response(serializer.data)
        else:
            return Response({
                'msg': 'Please Enter Valid Id'
            })
    if request.method == 'POST':
        request.POST._mutable = True
        myrequest = request.data
        print(type(myrequest))
        myrequest['stockProfileName'] = stock.id
        print(myrequest)
        stockOwnershipDirector_serializer = stockOwnershipDirectorSerializer(data=myrequest)
        if stockOwnershipDirector_serializer.is_valid():
            stockOwnershipDirector_serializer.save()
            response = stockOwnershipDirector.objects.filter(stockProfileName_id=stock.id)
            serializer = stockOwnershipDirectorSerializer(response, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(stockOwnershipDirector_serializer.errors)


@api_view(['GET'])
def stockInvestmentChecklistAPI(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    print(stock)
    if request.method == 'GET':
        response = stockInvestmentChecklist.objects.filter(stockProfileName_id=stock.id)
        if response.exists():
            serializer = stockInvestmentChecklistSerializer(response, many=True)
            return Response(serializer.data)

        else:
            return Response({
                'msg': 'Please Enter Valid Id'
            })


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def highlightsViewAPI(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    id = request.data.get('id')
    if request.method == 'DELETE':
        if id:
            response = highLights.objects.filter(id=id).first()
            if response:
                response.delete()
                return Response({
                    'msg': 'Data Deleted Successfully'
                })
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'id Field is Required'
            })
    if request.method == 'PUT':
        if id:
            response = highLights.objects.filter(id=id).first()
            if response:
                request.POST._mutable = True
                myrequest = request.data
                myrequest['stockProfileName'] = stock.id
                serializer = highLightsSerializer(response, data=myrequest)
                serializer_checker = serializer_valid(serializer)
                return Response(serializer_checker)
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'Id Filed Required'
            })
    if request.method == 'GET':
        if id:
            response = highLights.objects.filter(id=id).first()
            if response:
                serializer = highLightsSerializer(response)
                return Response(serializer.data)
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            response = highLights.objects.filter(stockProfileName_id=stock.id)
            serializer = highLightsSerializer(response, many=True)
            return Response(serializer.data)
    if request.method == 'POST':
        request.POST._mutable = True
        myrequest = request.data
        print(type(myrequest))
        myrequest['stockProfileName'] = stock.id
        highlight_serializer = highLightsSerializer(data=myrequest)
        if highlight_serializer.is_valid():
            highlight_serializer.save()
            response = highLights.objects.filter(stockProfileName_id=stock.id)
            serializer = highLightsSerializer(response, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(highlight_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def highlightsView(request):
    print("UUUUUUUUUUUUUUUUUUUUUUUUUUU")
    if request.method == 'POST':
        print("yaha aaya TTTTTTTTTTTTTTTTTTTTTTT")
        # print(request)
        stockProfile = request.POST.get('stockProfile')
        print(stockProfile)
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(highLights, pk=pkID)
        objForm = highLightsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Highlights sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['GET'])
def snapshotForBankNBFCsViewAPI(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = ""
        if stock:
            stock_detail = StockSerializer(stock)
            stock_detail = stock_detail.data
        if stock.status == 'draft' and not request.user.is_staff:
            return redirect('websiteApp:buypreIPOUrl')

        callingFunction = 'snapshot'
        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
        except:
            stockAdmInst = None
        # createStockAdmin = stockAdminForm(instance=stockAdmInst)
        # createStockAdminSnapshot = stockAdminSnapshotForm(instance=stockAdmInst)

        benGrahamOrDCFInst_detail = ""
        try:
            benGrahamOrDCFInst = benGrahamOrDCF.objects.get(stockProfileName=stock)
            if benGrahamOrDCFInst:
                #   for each in benGrahamOrDCFInst:
                benGrahamOrDCFInst_detail = benGrahamOrDCFSerializer(benGrahamOrDCFInst)
                benGrahamOrDCFInst_detail = benGrahamOrDCFInst_detail.data
        except:
            benGrahamOrDCFInst = None
        # benGrahamOrDCFCreate = benGrahamOrDCFForm(instance=benGrahamOrDCFInst)

        essentialInst_list = []
        essentialInst_detail = ""
        try:
            essentialInst = stockEssentials.objects.get(stockProfileName=stock)
            if essentialInst:
                #   for each in stockAdmInst:
                essentialInst_detail = stockEssentialsSerializer(essentialInst)
                essentialInst_detail = essentialInst_detail.data
        except:
            essentialInst = None
            essentialInst_list = None
            essentialInst_detail = ""
        stock_detail["stockProfileNameSE"] = essentialInst_detail
        financialFigureUnitsInst_detail = ""
        try:
            financialFigureUnitsInst = financialFigureUnits.objects.get(stockProfileName=stock)
            if financialFigureUnitsInst:
                financialFigureUnitsInst_detail = financialFigureUnitsSerializer(essentialInst)
                financialFigureUnitsInst_detail = financialFigureUnitsInst_detail.data
        except:
            financialFigureUnitsInst = None
            financialFigureUnitsInst_detail = ""

        stock_detail["stockProfileNameFFU"] = financialFigureUnitsInst_detail

        stockInvestmentChecklistInst_detail = ""
        try:
            stockInvestmentChecklistInst = stockInvestmentChecklist.objects.get(stockProfileName=stock)
            if stockInvestmentChecklistInst:
                #   for each in stockInvestmentChecklistInst:
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistSerializer(stockInvestmentChecklistInst)
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistInst_detail.data
        except:
            stockInvestmentChecklistInst_list = None

        stock_detail["stockProfileNameSIC"] = stockInvestmentChecklistInst_detail

        stockIPOInst_details = ""
        try:
            stockIPOInst = stockIPO.objects.get(stockProfileName=stock)
            if stockIPOInst:
                #   for each in stockIPOInst:
                stockIPOInst_details = stockIPOSerializer(stockIPOInst)
                stockIPOInst_details = stockIPOInst_details.data
        except:
            stockIPOInst = None

        stock_detail["stockProfileNameSI"] = stockIPOInst_details

        stockDetailsInst_details = ""
        try:
            stockDetailsInst = stockDetails.objects.get(stockProfileName=stock)
            if stockDetailsInst:
                #   for each in stockDetailsInst:
                stockDetailsInst_details = stockDetailsSerializer(stockDetailsInst)
                stockDetailsInst_details = stockDetailsInst_details.data
        except:
            stockDetailsInst = None

        stock_detail["stockProfileNameSD"] = stockDetailsInst_details
        # createStockDetails = stockDetailsFormMergerAcquistion(instance=stockDetailsInst)
        # createSubsidiariesBusModelStockDetails = stockDetailsSubsidiariesBusModelForm(instance=stockDetailsInst)
        # createProductStockDetails = stockDetailsProductForm(instance=stockDetailsInst)
        # createAssestStockDetails = stockDetailsAssestForm(instance=stockDetailsInst)
        # createIndustryOverviewStockDetails = stockDetailsIndustryOverviewForm(instance=stockDetailsInst)
        # createStockAbout = stockDetailsAboutForm(instance=stockDetailsInst)
        # createawardsDescription = stockDetailsAwardForm(instance=stockDetailsInst)
        # createSSOTDescription = stockDetailsSSOTForm(instance=stockDetailsInst)

        revenueBreakupInst = stockRevenueBreakUp.objects.filter(stockProfileName=stock)
        revenueBreakupInst_list = []
        if revenueBreakupInst:
            for each in revenueBreakupInst:
                revenueBreakupInst_ser = stockRevenueBreakUpSerializer(each)
                revenueBreakupInst_list.append(revenueBreakupInst_ser.data)
        # viewStockRevenueBreakUpForm = stockRevenueBreakUpForm()
        stockFundingRoundsInst_list = []
        try:
            stockFundingRoundsInst = stockFundingRounds.objects.filter(stockProfileName=stock).order_by(
                '-dateOfInvestment')
            if stockFundingRoundsInst:
                for each in stockFundingRoundsInst:
                    stockFundingRoundsInst_ser = stockFundingRoundsSerializer(each)
                    stockFundingRoundsInst_list.append(stockFundingRoundsInst_ser.data)
        except:
            stockFundingInst = None

        stockFundingInst_detail = ""
        try:
            stockFundingInst = stockFunding.objects.get(stockProfileName=stock)
            if stockFundingInst:
                #   for each in stockFundingInst:
                stockFundingInst_detail = stockFundingSerializer(stockFundingInst)
                stockFundingInst_detail = stockFundingInst_detail.data
        except:
            stockFundingInst = None

        stock_detail['stockProfileNameSF'] = stockFundingInst_detail

        try:
            promotorHolding = stockOwnershipPattern.objects.get(stockProfileName=stock, year=currentYear)
            promotorHolding = promotorHolding.totalPromoterholdingValue
        except:
            promotorHolding = None
        try:
            # latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
            latestProfitAndLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')

            totalRevCY = latestProfitAndLoss.totalRevenue
            patCY = latestProfitAndLoss.netIncome
            epsCY = latestProfitAndLoss.basicEPS
            dps = latestProfitAndLoss.DPS
        except:
            totalRevCY = None
            patCY = None
            epsCY = None
            dps = None
        try:
            latestCashFlow = stockCashFlow.objects.filter(stockProfileName=stock).latest('year')
            cashFlowOperationsCY = latestCashFlow.cashFromOperatingActivities
            cashFlowFinancingCY = latestCashFlow.cashFromFinancingActivities
        except:
            cashFlowOperationsCY = None
            cashFlowFinancingCY = None

        categoryForEss = categoryOptions.objects.all().order_by('name')
        categoryForEss_list = []
        if categoryForEss:
            for each in categoryForEss:
                categoryForEss = categoryOptionsSerializer(each)
                categoryForEss_list.append(categoryForEss.data)
        sectorForEss = sectorOptions.objects.all().order_by('name')
        sectorForEss_list = []
        if sectorForEss:
            for each in sectorForEss:
                categoryForEss = sectorOptionsSerializer(each)
                sectorForEss_list.append(categoryForEss.data)
        subSectorForEss = subSectorOptions.objects.all().order_by('name')
        subSectorForEss_list = []
        if subSectorForEss:
            for each in subSectorForEss:
                subSectorForEss = subSectorOptionsSerializer(each)
                subSectorForEss_list.append(subSectorForEss.data)

        # Required changes in formuals Calculation starts  - done
        returnedGrowthROEVal = ROEgrowthCalculatorFrBankNBFCs(stock)
        intrinsicVal = intrinsicFormula(stock, forNBFC=True)
        # intrinsicVal = intrinsicFormulafrBankNBFCs(stock)
        returnedRevenueGrowthAlgoProgrammedData, processedNetProfitGrowthTextual = calGrowthTemplateDataViewFrBankNBFcs(
            stock, requestFrom='snapshot')
        # compoundSalesGrowth = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
        # compoundProfitGrowth = calculateProgrammedGrowth(processedNetProfitGrowthTextual)
        profitAndLossQuerySet = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')
        revenueGrowth = calculateGrowthNew(profitAndLossQuerySet, 'totalRevenue')
        compoundProfitGrowth = calculateGrowthNew(profitAndLossQuerySet, 'netIncome')
        # Required changes in formuals Calculation ends - done

        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        stockTransferDepositoryOptions_list = []
        try:
            if despositoryOptions:
                for each in despositoryOptions:
                    stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                    stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
        except:
            despositoryOptions = None
            stockTransferDepositoryOptions_list = []
        saleTypeOptions_list = []
        try:
            if saleType:
                for each in saleType:
                    saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                    saleTypeOptions_list.append(saleTypeOptions_ser.data)
        except:
            saleType = None
            saleTypeOptions_list = []

        bookValues_detail = ""
        try:
            bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
            if bookValues:
                #    for each in bookValues:
                bookValues_detail = bookValueDataSerializer(bookValues)
                bookValues_detail = bookValues_detail.data

            bookValYear = bookValues.year
            # totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=bookValYear)
            totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=bookValYear)
            bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
        except:
            bookValues = bookValueCal = None

        fundingRoundsUnitInst_detail = ""
        try:
            fundingRoundsUnitInst = get_object_or_404(foundingRoundsFigureUnits, stockProfileName=stock)
            if fundingRoundsUnitInst:
                fundingRoundsUnitInst_detail = foundingRoundsFigureUnitsSerializer(fundingRoundsUnitInst)
                fundingRoundsUnitInst_detail = fundingRoundsUnitInst_detail.data
        except:
            fundingRoundsUnitInst = None
            fundingRoundsUnitInst_detail = ""

        fundingDetailsVisibilityInst_detail = ""
        try:
            fundingDetailsVisibilityInst = get_object_or_404(fundingDetailsVisibility, stockProfileName=stock)
            if fundingDetailsVisibilityInst:
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilitySerializer(fundingDetailsVisibilityInst)
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilityInst_detail.data
        except:
            fundingDetailsVisibilityInst = None
            fundingDetailsVisibilityInst_detail = ""

        stock_detail['stockProfileNameFDVI'] = fundingDetailsVisibilityInst_detail

        # fundingDetailsVisibilityCreate = fundingDetailsVisibilityForm()

        currentStockPrice = localOrScreenerPriceView(stock)

        if essentialInst:
            totalSharesInst = essentialInst.totalShares
        else:
            totalSharesInst = 0

        try:
            stockProfitAndLossInst = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            basicEps = stockProfitAndLossInst.basicEPS
            dilutedEps = stockProfitAndLossInst.dilutedEPS
        except:
            basicEps = 1
            dilutedEps = 1

        eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
        decimalEPS = return_decimal_or_0(eps)
        if decimalEPS == 0:
            decimalEPS = 1
        try:
            PEvalue = round((currentStockPrice / decimalEPS), 2)
        except:
            PEvalue = None

        if bookValues:
            bookVal = bookValueCal
        else:
            bookVal = 1
        try:
            PBvalue = round((currentStockPrice / bookVal), 2)
        except:
            PBvalue = None

        try:
            earningsYield = round((epsCY / currentStockPrice) * 100, 2)
        except:
            earningsYield = None

        try:
            dividendYield = round((dps / currentStockPrice) * 100, 2)
        except:
            dividendYield = None
        try:
            latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            aumVals = latestBalanceSheet.aum
            aumGrowthVals = round(latestBalanceSheet.aumGrowth, 2)
        except:
            aumVals = None
            aumGrowthVals = None

        researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
        researchReportFAQsInst_list = []
        if len(researchReportFAQsInst):
            for each in researchReportFAQsInst:
                researchReportFAQs_serial = researchReportFAQsSerializer(each)
                researchReportFAQsInst_list.append(researchReportFAQs_serial.data)
        # researchReportFAQsInstForm = researchReportFAQsForm()

        # Enterprise Value
        cashAndShortTermEqui = minorityInt = 0
        try:
            stockBalanceSheetLatestObj = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            cashAndShortTermEqui = stockBalanceSheetLatestObj.cashAndCashEquivalents
            minorityInt = stockBalanceSheetLatestObj.minorityInterest

        except:
            pass
        balWithRBI = prefEquity = 0
        try:
            balWithRBI = essentialInst.balance_with_RBI
            prefEquity = essentialInst.preference_equity
        except:
            pass
        if not balWithRBI:
            balWithRBI = 0
        if not prefEquity:
            prefEquity = 0
        lgTermBorrow = curPortionOfLongTermDebt = srtTermBorrowings = leasLiability = 0
        try:
            latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            if latestBalanceSheet.longTermBorrowings:
                lgTermBorrow = Decimal(latestBalanceSheet.longTermBorrowings)
            if latestBalanceSheet.currentPortionOfLongTermDebt:
                curPortionOfLongTermDebt = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
            if latestBalanceSheet.shortTermBorrowings:
                srtTermBorrowings = Decimal(latestBalanceSheet.shortTermBorrowings)
            if latestBalanceSheet.leaseLiability:
                leasLiability = Decimal(latestBalanceSheet.leaseLiability)
        except:
            pass
        totalDebt = lgTermBorrow + srtTermBorrowings + leasLiability + curPortionOfLongTermDebt
        try:
            marketCap = (totalSharesInst * currentStockPrice) / 10000000
        except:
            marketCap = None
        try:
            marketCapForEnterprise = numberConversion(marketCap, currentSystem='Cr',
                                                      convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            marketCapForEnterprise = None
        enterpriseVal = returnDecimalOrZero(marketCapForEnterprise) - (
                returnDecimalOrZero(cashAndShortTermEqui) - returnDecimalOrZero(balWithRBI)) + returnDecimalOrZero(
            totalDebt) + returnDecimalOrZero(prefEquity) + returnDecimalOrZero(minorityInt)
        try:
            enterpriseVal = numberConversion(enterpriseVal, currentSystem=stock.stockProfileNameFFU.financialNumbers,
                                             convertTo='Cr')
        except:
            pass

        totalShareYearlyDataInst = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                       shareType='financial_year').order_by('year')
        totalShareYearlyDataInst_list = []
        if len(totalShareYearlyDataInst):
            for each in totalShareYearlyDataInst:
                totalShareYearly_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInst_list.append(totalShareYearly_serial.data)
        totalShareYearlyDataInstConvertible = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                                  shareType='convertible_equity').order_by(
            'year')
        totalShareYearlyDataInstConvertible_list = []
        if len(totalShareYearlyDataInstConvertible):
            for each in totalShareYearlyDataInstConvertible:
                totalShareYearlyData_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInstConvertible_list.append(totalShareYearlyData_serial.data)
        # totalShareYearlyDataInstForm = totalShareYearlyDataForm()
        # commonFAQInstForm = commonFAQForm()
        commonFAQInst = commonFAQ.objects.all().order_by('id')
        commonFAQInst_list = []
        if len(commonFAQInst):
            for each in commonFAQInst:
                commonFAQInst_serial = commonFAQSerializer(each)
                commonFAQInst_list.append(commonFAQInst_serial.data)
        # researchReportFAQsInstForm = researchReportFAQsForm()
        context = {
            'bookValues': bookValues_detail,
            # 'essentialInst': essentialInst_list,
            # 'createStockEssentials': createStockEssentials,
            # 'createStockEssentialsBottom': createStockEssentialsBottom,
            # 'stockInvestmentChecklistInst': stockInvestmentChecklistInst_list,
            # 'createstockInvestmentChecklist': createstockInvestmentChecklist,
            # 'stockIPOInst': stockIPOInst_list,
            # 'createStockIPO': createStockIPO,
            # 'stockDetailsInst': stockDetailsInst_list,
            # 'createStockDetails': createStockDetails,
            # 'createSubsidiariesBusModelStockDetails': createSubsidiariesBusModelStockDetails,
            # 'createProductStockDetails': createProductStockDetails,
            # 'createAssestStockDetails': createAssestStockDetails,
            # 'createIndustryOverviewStockDetails': createIndustryOverviewStockDetails,
            # 'stockFundingInst': stockFundingInst_list,
            # 'createStockFunding': createStockFunding,
            'stockFundingRoundsInst': stockFundingRoundsInst_list,
            # 'createStockFundingRounds': createStockFundingRounds,
            'promotorHolding': promotorHolding,
            'stockAdmInst': stockAdmInst_detail,
            # 'createStockAdmin': createStockAdmin,
            # 'createStockAdminSnapshot': createStockAdminSnapshot,
            # 'createStockAbout': createStockAbout,
            # 'createawardsDescription': createawardsDescription,
            # 'createSSOTDescription': createSSOTDescription,
            'compoundSalesGrowth': revenueGrowth,
            'compoundProfitGrowth': compoundProfitGrowth,
            'totalRevCY': totalRevCY,
            'patCY': patCY,
            'epsCY': epsCY,
            'cashFlowOperationsCY': cashFlowOperationsCY,
            'cashFlowFinancingCY': cashFlowFinancingCY,
            'categoryForEss': categoryForEss_list,
            'sectorForEss': sectorForEss_list,
            'subSectorForEss': subSectorForEss_list,
            'returnedGrowthROEVal': returnedGrowthROEVal,
            'intrinsicVal': intrinsicVal,
            'revenueBreakupInst': revenueBreakupInst_list,
            # 'viewStockRevenueBreakUpForm': viewStockRevenueBreakUpForm,
            'despositoryOptions': stockTransferDepositoryOptions_list,
            'saleType': saleTypeOptions_list,
            'stock': stock_detail,
            'fundingRoundsUnitInst': fundingRoundsUnitInst_detail,
            # 'fundingRoundsUnitCreate': fundingRoundsUnitCreate,
            # 'fundingDetailsVisibilityInst': fundingDetailsVisibilityInst,
            # 'fundingDetailsVisibilityCreate': fundingDetailsVisibilityCreate,
            'benGrahamOrDCFInst': benGrahamOrDCFInst_detail,
            # 'benGrahamOrDCFForm': benGrahamOrDCFCreate,
            'marketCap': marketCap,
            'PEvalue': PEvalue,
            'PBvalue': PBvalue,
            'earningsYield': earningsYield,
            'dividendYield': dividendYield,
            'bookValueCal': bookValueCal,
            'aumVals': aumVals,
            'aumGrowthVals': aumGrowthVals,
            'researchReportFAQsInst': researchReportFAQsInst_list,
            # 'researchReportFAQsInstForm': researchReportFAQsInstForm,
            'enterpriseVal': enterpriseVal,
            'totalShareYearlyDataInst': totalShareYearlyDataInst_list,
            'totalShareYearlyDataInstConvertible': totalShareYearlyDataInstConvertible_list,
            # 'totalShareYearlyDataInstForm': totalShareYearlyDataInstForm,
            'commonFAQInst': commonFAQInst_list,
            # 'commonFAQInstForm': commonFAQInstForm,
            # 'researchReportFAQsInstForm': researchReportFAQsInstForm,
        }

        return Response({'response': context})


@api_view(['GET'])
def peersViewapi(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = {}
        if stock:
            stock_detail = StockSerializer(stock)
            stock_detail = stock_detail.data
        if stock.status == 'draft' and not request.user.is_staff:
            return redirect('websiteApp:buypreIPOUrl')

        # renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
        # if renderBankNBFCsTemplates:
        # 	return peersForBankNBFCView(request, slug)
        netProfitMarginCY = revenueCY = 0.00
        allStockList_list = []
        allStockList = stockBasicDetail.objects.all()
        if allStockList:
            for each in allStockList:
                allStockList_ser = StockSerializer(each)
                allStockList_list.append(allStockList_ser.data)
        yearCY = onlyRevenue = ebitda = None
        revenuePeersCompanyList_list = []
        revenuePeersCompanyList = peersCompanyLinking.objects.filter(stockProfileName=stock)
        if revenuePeersCompanyList:
            for each in revenuePeersCompanyList:
                revenuePeersCompanyList_ser = peersCompanyLinkingSerializer(each)
                revenuePeersCompanyList_list.append(revenuePeersCompanyList_ser.data)
        totalInvPY = totalInvCY = totalRevCY = totalIntangiblesCY = totalIntangiblesPY = totalAssetCY = totalAssetPY = netIncomeCY = totalEquityCY = totalEquityPY = EBITCY = longTermDebtCY = longTermDebtPY = 0.00
        totalAssetTurnoverRatioCY = totalFixedAssetTurnoverRatioCY = ROECY = ROCECY = debtToEquity = 0.00
        totalLngDebtCY = currPortLngTermDebtCY = currPortionLeasesCY = lngTermPortionOfLeasesCY = 0.0
        totalLngDebtPY = currPortLngTermDebtPY = currPortionLeasesPY = lngTermPortionOfLeasesPY = 0.0
        totalNonCurrentLiabilityCY = totalNonCurrentLiabilityPY = 0.0

        # revenueGraphData = {}
        screenerDict = {}
        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
        except:
            stockAdmInst = None
        try:
            latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
        except:
            latestProfitAndLoss = 0.00
        try:
            latestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
        except:
            latestBalanceSheet = 0.00
        try:
            secondLatestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('-year')[1:2]
        except:
            secondLatestBalanceSheet = 0.00
        cashAndShortTermBalSheet = minorityInterestVal = totalCalculatedLnDebtCY = 0
        if latestBalanceSheet:
            cashAndShortTermBalSheet = latestBalanceSheet.cashAndShortTermInvestments
            minorityInterestVal = latestBalanceSheet.minorityInterest
            for item in secondLatestBalanceSheet:
                if item:
                    if latestProfitAndLoss != 0.00:
                        if latestProfitAndLoss.revenue:
                            yearCY = latestProfitAndLoss.year
                            if latestProfitAndLoss.revenue:
                                totalRevCY = Decimal(latestProfitAndLoss.revenue)
                            if latestBalanceSheet.totalInventory:
                                totalInvCY = Decimal(latestBalanceSheet.totalInventory)
                            if item.totalInventory:
                                totalInvPY = Decimal(item.totalInventory)
                            if latestBalanceSheet.otherIntangibleAssests:
                                totalIntangiblesCY = Decimal(latestBalanceSheet.otherIntangibleAssests)
                            if item.otherIntangibleAssests:
                                totalIntangiblesPY = Decimal(item.otherIntangibleAssests)
                            if latestBalanceSheet.totalAssets:
                                totalAssetCY = Decimal(latestBalanceSheet.totalAssets)
                            if item.totalAssets:
                                totalAssetPY = Decimal(item.totalAssets)
                            if latestProfitAndLoss.netIncome:
                                netIncomeCY = Decimal(latestProfitAndLoss.netIncome)
                            if latestBalanceSheet.totalEquity:
                                totalEquityCY = Decimal(latestBalanceSheet.totalEquity)
                            if item.totalEquity:
                                totalEquityPY = Decimal(item.totalEquity)
                            if latestProfitAndLoss.pbit:
                                EBITCY = Decimal(latestProfitAndLoss.pbit)
                            if latestBalanceSheet.totalLongTermDebt:
                                totalLngDebtCY = Decimal(latestBalanceSheet.totalLongTermDebt)
                            if item.totalLongTermDebt:
                                totalLngDebtPY = Decimal(item.totalLongTermDebt)
                            if latestBalanceSheet.currentPortionOfLongTermDebt:
                                currPortLngTermDebtCY = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
                            if item.currentPortionOfLongTermDebt:
                                currPortLngTermDebtPY = Decimal(item.currentPortionOfLongTermDebt)
                            if latestBalanceSheet.currentPortionOfLeases:
                                currPortionLeasesCY = Decimal(latestBalanceSheet.currentPortionOfLeases)
                            if item.currentPortionOfLeases:
                                currPortionLeasesPY = Decimal(item.currentPortionOfLeases)
                            if latestBalanceSheet.longTermPortionOfLeases:
                                lngTermPortionOfLeasesCY = Decimal(latestBalanceSheet.longTermPortionOfLeases)
                            if item.longTermPortionOfLeases:
                                lngTermPortionOfLeasesPY = Decimal(item.longTermPortionOfLeases)
                            if latestBalanceSheet.nonCurrentLiabilities:
                                totalNonCurrentLiabilityCY = Decimal(latestBalanceSheet.nonCurrentLiabilities)
                            if item.nonCurrentLiabilities:
                                totalNonCurrentLiabilityPY = Decimal(item.nonCurrentLiabilities)

                            totalCalculatedLnDebtCY = Decimal(totalLngDebtCY) + Decimal(
                                currPortLngTermDebtCY) + Decimal(
                                currPortionLeasesCY) + Decimal(lngTermPortionOfLeasesCY)
                            totalCalculatedLnDebtPY = Decimal(totalLngDebtPY) + Decimal(
                                currPortLngTermDebtPY) + Decimal(
                                currPortionLeasesPY) + Decimal(lngTermPortionOfLeasesPY)

                            totalAssetTurnoverRatioCY = round(
                                totalAssetTurnoverRatioFormula(totalRevCY, totalAssetCY, totalAssetPY), 2)
                            totalFixedAssetTurnoverRatioCY = round(
                                totalFixedAssetTurnoverRatioFormula(totalRevCY, totalInvCY, totalInvPY), 2)
                            ROECY = round(ROEFormula(netIncomeCY, totalEquityCY, totalEquityPY), 2)
                            ROCECY = round(ROCEFormula(EBITCY, totalEquityCY, totalEquityPY, totalNonCurrentLiabilityCY,
                                                       totalNonCurrentLiabilityPY), 2)
                            debtToEquity = round(
                                debtToEquityFormula(totalCalculatedLnDebtCY, totalCalculatedLnDebtPY, totalEquityCY,
                                                    totalEquityPY), 2)
        if latestProfitAndLoss:
            if latestProfitAndLoss.totalRevenue:
                revenueCY = round(latestProfitAndLoss.totalRevenue, 2)
            if latestProfitAndLoss.revenue:
                onlyRevenue = round(latestProfitAndLoss.revenue, 2)
            if latestProfitAndLoss.ebidta:
                ebitda = round(latestProfitAndLoss.ebidta, 2)
            # changes in NPM - Peers starts (Formula changed - It should be revenue of operations insted of Total Revenue )
            netProfitMarginCY = round(
                netProfitMarginFormula(latestProfitAndLoss.netIncome, latestProfitAndLoss.revenue), 2)
        # changes in NPM - Peers ends

        peRatioCS, pbRatioCS = currentStockPEPBView(stock)
        try:
            essentialInst = stockEssentials.objects.get(stockProfileName=stock)
        except:
            essentialInst = None
        marketCapCS = marketCapView(stock)
        if onlyRevenue == 0 or onlyRevenue == None:
            onlyRevenue = 1

        marketCapBySales = return_val_or_0(marketCapCS) / return_val_or_1(onlyRevenue)

        if essentialInst:
            enterpriseValueInst = essentialInst.enterpriseValue
            balanceWithRBIVal = essentialInst.balance_with_RBI
            preferenceEquityVal = essentialInst.preference_equity
        else:
            enterpriseValueInst = 0
            balanceWithRBIVal = preferenceEquityVal = 0
        if ebitda == 0:
            ebitda = 1

        try:
            if stock.stockProfileNameFFU.financialNumbers == 'L':
                marketCapCS = numberConversion(marketCapCS, currentSystem='Cr',
                                               convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        enterpriseVal = return_val_or_0(marketCapCS) - (
                return_val_or_0(cashAndShortTermBalSheet) - return_val_or_0(balanceWithRBIVal)) + return_val_or_0(
            totalCalculatedLnDebtCY) + return_val_or_0(preferenceEquityVal) + return_val_or_0(minorityInterestVal)

        # numberConversion
        # enterpriseVal = numberConversion(enterpriseVal, currentSystem='L', convertTo=stock.stockProfileNameFFU.financialNumbers)
        evByEbitda = round(return_val_or_0(enterpriseVal) / return_val_or_1(ebitda), 2)
        # conversion

        try:
            if stock.stockProfileNameFFU.financialNumbers == 'L':
                marketCapBySales = numberConversion(marketCapBySales, currentSystem='Cr',
                                                    convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        marketCapBySales = round(marketCapBySales, 2)

        stockname = str(stock_detail.get("stockName"))
        screenerDict = {stockname:
            {
                'id': stock.id,
                'type': 'current',
                'revenue': revenueCY,
                'netProfitMargin': netProfitMarginCY,
                'assetTurnoverRation': totalAssetTurnoverRatioCY,
                'totalFixedAssetTurnoverRatio': totalFixedAssetTurnoverRatioCY,
                'ROE': ROECY,
                'ROCE': ROCECY,
                'deptToEquity': debtToEquity,
                'peGraph': peRatioCS,
                'pbGraph': pbRatioCS,
                'marketCap': round(return_val_or_0(marketCapCS), 2),
                'marketCapBySales': marketCapBySales,
                'evByEbitda': evByEbitda,
            }
        }

        fetchForYear = int(currentYear) - 1
        if latestProfitAndLoss:
            if latestProfitAndLoss.year:
                fetchForYear = latestProfitAndLoss.year
        for company in revenuePeersCompanyList:
            if company.stockStatus == 'Listed' and company.screenerLink:
                screenerDict[company.stockName] = crawlScreenerView(company, fetchForYear=fetchForYear)
            else:
                yearlyData = peerLinkingYearlyData.objects.filter(screenerCompany=company)
                yearlyData_list = []
                if yearlyData:
                    for each in yearlyData:
                        yearlyData_serial = peerLinkingYearlyDataSerializer(each)
                        yearlyData_list.append(yearlyData_serial.data)
                try:
                    stockYearData = yearlyData.get(year=fetchForYear)
                    screenerDict[company.stockName] = {
                        'id': company.pk,
                        'type': company.stockStatus,
                        'fetchedUrl': '',
                        'revenue': stockYearData.revenue,
                        'netProfitMargin': stockYearData.netProfitMargin,
                        'assetTurnoverRation': stockYearData.assetTurnoverRation,
                        'ROE': stockYearData.ROE,
                        'ROCE': stockYearData.ROCE,
                        'deptToEquity': stockYearData.deptToEquity,
                        'peGraph': stockYearData.peRatio,
                        'pbGraph': stockYearData.pbRatio,
                        'marketCap': stockYearData.marketCap,
                        'marketCapBySales': stockYearData.marketCapBySales,
                        'enterpriseVal': stockYearData.enterpriseValue,
                        'evByEbitda': stockYearData.evByEbitda,
                        'cashAndShortTermEquivalents': stockYearData.cashAndShortTermCashEquivalents,
                        'PreferenceEquity': stockYearData.PreferenceEquity,
                        'totalMinorityInterest': stockYearData.totalMinorityInterest,
                        'longTermMarketableSecurities': stockYearData.longTermMarketableSecurities,
                        'yearNotAvailable': '',
                        'yearlyData': yearlyData_list,
                    }
                except:
                    screenerDict[company] = {
                        'id': company.pk,
                        'type': company.stockStatus,
                        'fetchedUrl': '',
                        'revenue': 0,
                        'netProfitMargin': 0,
                        'assetTurnoverRation': 0,
                        'ROE': 0,
                        'ROCE': 0,
                        'deptToEquity': 0,
                        'peGraph': 0,
                        'pbGraph': 0,
                        'marketCap': 0,
                        'marketCapBySales': 0,
                        'enterpriseVal': 0,
                        'evByEbitda': 0,
                        'cashAndShortTermEquivalents': 0,
                        'PreferenceEquity': 0,
                        'totalMinorityInterest': 0,
                        'longTermMarketableSecurities': 0,
                        'yearNotAvailable': '',
                        'yearlyData': yearlyData,
                    }
        stockPeersDescInst_detail = ""
        try:
            stockPeersDescInst = stockPeers.objects.get(stockProfileName=stock)
            if stockPeersDescInst:
                stockPeersDescInst_detail = stockPeersSerializer(stockPeersDescInst)
                stockPeersDescInst_detail = stockPeersDescInst_detail.data
        except:
            stockPeersDescInst = None
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        if revenueCY == 0.00 and netProfitMarginCY == 0.00 and \
                totalAssetTurnoverRatioCY == 0.00 and totalFixedAssetTurnoverRatioCY == 0.00 and \
                ROECY == 0.00 and ROCECY == 0.00 and debtToEquity == 0.00 and peRatioCS and \
                pbRatioCS == 0.00 and marketCapCS == 0.00 and marketCapBySales == 0.00 and evByEbitda == 0.00:
            visiblity = False
        else:
            visiblity = True
        context = {
            'stock': stock_detail,
            'allStockList': allStockList_list,
            'stockPeersDescInst': stockPeersDescInst_detail,
            'stockAdmInst': stockAdmInst_detail,
            'despositoryOptions': despositoryOptions,
            'saleType': saleType,
            'visible': visiblity,
            'screenerDict': screenerDict,
            'year': yearCY,
        }
        return Response({'response': context})


@api_view(['GET'])
def financialViewapi(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = ""
        if stock:
            stock_detail = StockSerializer(stock)
            stock_detail = stock_detail.data
        if stock.status == 'draft' and not request.user.is_staff:
            return redirect('websiteApp:buypreIPOUrl')

        renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
        if renderBankNBFCsTemplates:
            return redirect("stockApp:financialForBankNBFCsApi", slug)

        includeFile = 'UI/financialProfitAndLoss.html'
        activeNavTab = request.GET.get('nav')
        if activeNavTab:
            if activeNavTab == 'profit-and-loss':
                includeFile = 'UI/financialProfitAndLoss.html'
            elif activeNavTab == 'cash-flow':
                includeFile = 'UI/financialCashFlow.html'
            elif activeNavTab == 'balance-sheet':
                includeFile = 'UI/financialBalanceSheet.html'
        fallBackFile = 'UI/financialProfitAndLoss.html'
        tempToInclude = select_template([includeFile, fallBackFile])
        despositoryOptions, saleType = rightSideMenuObjs_serialized()

        financialStatementsFrProfitAndLossInst_list = []
        financialStatementsFrProfitAndLossInst = financialStatementsFrProfitAndLoss.objects.filter(
            stockProfileName=stock)
        if financialStatementsFrProfitAndLossInst:
            for each in financialStatementsFrProfitAndLossInst:
                financialStatementsFrProfitAndLossInst_ser = financialStatementsFrProfitAndLossSerializer(each)
                financialStatementsFrProfitAndLossInst_list.append(financialStatementsFrProfitAndLossInst_ser.data)

        financialStatementsFrBalanceSheetInst_list = []
        financialStatementsFrBalanceSheetInst = financialStatementsFrBalanceSheet.objects.filter(stockProfileName=stock)
        if financialStatementsFrBalanceSheetInst:
            for each in financialStatementsFrBalanceSheetInst:
                financialStatementsFrBalanceSheetInst_ser = financialStatementsFrBalanceSheetSerializer(each)
                financialStatementsFrBalanceSheetInst_list.append(financialStatementsFrBalanceSheetInst_ser.data)

        financialStatementsFrCashFlowInst_list = []
        financialStatementsFrCashFlowInst = financialStatementsFrCashFlow.objects.filter(stockProfileName=stock)
        if financialStatementsFrCashFlowInst:
            for each in financialStatementsFrCashFlowInst:
                financialStatementsFrCashFlowInst_ser = financialStatementsFrCashFlowSerializer(each)
                financialStatementsFrCashFlowInst_list.append(financialStatementsFrCashFlowInst_ser.data)

        financialCompanyUpdatesInst_list = []
        financialCompanyUpdatesInst = financialCompanyUpdates.objects.filter(stockProfileName=stock).order_by('title')
        if financialCompanyUpdatesInst:
            for each in financialCompanyUpdatesInst:
                financialCompanyUpdatesInst_ser = financialStatementsFrCashFlowSerializer(each)
                financialCompanyUpdatesInst_list.append(financialCompanyUpdatesInst_ser.data)

        stockProfitAndLossInst_list = []
        stockProfitAndLossInst = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')
        if len(stockProfitAndLossInst):
            for each in stockProfitAndLossInst:
                stockProfitAndLossInst_ser = stockProfitAndLossSerializer(each)
                stockProfitAndLossInst_list.append(stockProfitAndLossInst_ser.data)

        stockBalanceSheetInst_list = []
        stockBalanceSheetInst = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('year')
        if stockBalanceSheetInst:
            for each in stockBalanceSheetInst:
                stockBalanceSheetInst_ser = stockBalanceSheetSerializer(each)
                stockBalanceSheetInst_list.append(stockBalanceSheetInst_ser.data)

        stockCashFlowInst_list = []
        stockCashFlowInst = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')
        if stockCashFlowInst:
            for each in stockCashFlowInst:
                stockCashFlowInst_ser = stockCashFlowSerializer(each)
                stockCashFlowInst_list.append(stockCashFlowInst_ser.data)

        stockDeckAndDocsInst_list = []
        stockDeckAndDocsInst = stockDeckAndDocs.objects.filter(stockProfileName=stock).order_by('-id')
        if stockCashFlowInst:
            for each in stockDeckAndDocsInst:
                stockDeckAndDocsInst_ser = stockDeckAndDocsSerializer(each)
                stockDeckAndDocsInst_list.append(stockDeckAndDocsInst_ser.data)

        figureUnitInst_list = ""
        try:
            figureUnitInst = get_object_or_404(financialFigureUnits, stockProfileName=stock)
            if figureUnitInst:
                figureUnitInst_detail = financialFigureUnitsSerializer(figureUnitInst)
                figureUnitInst_detail = figureUnitInst_detail.data
        except:
            figureUnitInst = None

        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
        except:
            stockAdmInst = None

        annualReportsDHRPInst_detail = ""
        try:
            annualReportsDHRPInst = annualReportsDHRP.objects.get(stockProfileName=stock)
            if annualReportsDHRPInst:
                annualReportsDHRPInst_detail = annualReportsDHRPSerializer(annualReportsDHRPInst)
                annualReportsDHRPInst_detail = annualReportsDHRPInst_detail.data
        except:
            annualReportsDHRPInst = None

        balanceSheetTTMInst_detail = ""
        try:
            balanceSheetTTMInst = stockBalanceSheetTTM.objects.get(stockProfileName=stock)
            if balanceSheetTTMInst:
                balanceSheetTTMInst_detail = stockBalanceSheetTTMSerializer(balanceSheetTTMInst)
                balanceSheetTTMInst_detail = balanceSheetTTMInst_detail.data
        except:
            balanceSheetTTMInst = None

        profitAndLossTTMInst_detail = ""
        try:
            profitAndLossTTMInst = stockProfitAndLossTTM.objects.get(stockProfileName=stock)
            if profitAndLossTTMInst:
                profitAndLossTTMInst_detail = stockProfitAndLossTTMSerializer(profitAndLossTTMInst)
                profitAndLossTTMInst_detail = profitAndLossTTMInst_detail.data
        except:
            profitAndLossTTMInst = None

        cashFlowTTMInst_detail = ""
        try:
            cashFlowTTMInst = stockCashFlowTTM.objects.get(stockProfileName=stock)
            if cashFlowTTMInst:
                cashFlowTTMInst_detail = stockCashFlowTTMSerializer(cashFlowTTMInst)
                cashFlowTTMInst_detail = cashFlowTTMInst_detail.data
        except:
            cashFlowTTMInst = None

        # description field for SEO - starts
        stockFinBalanceSheetSEOInst_detail = ""
        try:
            stockFinBalanceSheetSEOInst = stockFinBalanceSheetSEO.objects.get(stockProfileName=stock)
            if stockFinBalanceSheetSEOInst:
                stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOSerializer(stockFinBalanceSheetSEOInst)
                stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOInst_detail.data
        except:
            stockFinBalanceSheetSEOInst = None
        # description field for SEO - ends

        context = {
            'stock': stock_detail,
            'includeFile': includeFile,
            'financialStatementsFrProfitAndLossInst': financialStatementsFrProfitAndLossInst_list,
            'financialStatementsFrBalanceSheetInst': financialStatementsFrBalanceSheetInst_list,
            'financialStatementsFrCashFlowInst': financialStatementsFrCashFlowInst_list,
            'financialCompanyUpdatesInst': financialCompanyUpdatesInst_list,
            'stockProfitAndLossInst': stockProfitAndLossInst_list,
            'stockBalanceSheetInst': stockBalanceSheetInst_list,
            'stockCashFlowInst': stockCashFlowInst_list,
            'stockAdmInst': stockAdmInst_detail,
            'figureUnitInst': figureUnitInst_list,
            'despositoryOptions': despositoryOptions,
            'saleType': saleType,
            'annualReportsDHRPInst': annualReportsDHRPInst_detail,
            'balanceSheetTTMInst': balanceSheetTTMInst_detail,
            'profitAndLossTTMInst': profitAndLossTTMInst_detail,
            'cashFlowTTMInst': cashFlowTTMInst_detail,
            'stockFinBalanceSheetSEOInst': stockFinBalanceSheetSEOInst_detail,
            'stockDeckAndDocsInst': stockDeckAndDocsInst_list,
        }

        return Response({'response': context})


@api_view(['GET'])
def eventsViewapi(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    if request.method == 'GET':
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_ser = stockAdminSerializer(stockAdmInst)
                stockAdmInst = stockAdmInst_ser.data
        except:
            stockAdmInst = None

        stockEventsDividendInst = stockEventsDividend.objects.filter(stockProfileName=stock).order_by(
            '-exDateFrDividend')
        pastDividents = []
        futureDividents = []
        for item in stockEventsDividendInst:
            if str(item.exDateFrDividend) > today:
                futureDividents.append(EmployeeEncoder().encode(item))
            else:
                pastDividents.append(EmployeeEncoder().encode(item))
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        stockEventsCorpActionsInst = stockEventsCorpActions.objects.filter(stockProfileName=stock).order_by(
            '-exDateFrCorporate')
        pastCorpActions = []
        futureCorpActions = []
        for item in stockEventsCorpActionsInst:
            if str(item.exDateFrCorporate) > today:
                futureCorpActions.append(EmployeeEncoder().encode(item))
            else:
                pastCorpActions.append(EmployeeEncoder().encode(item))

        stockEventsAnnouncementsInst = stockEventsAnnouncements.objects.filter(stockProfileName=stock).order_by(
            '-dateFrAnnouncement')
        pastAnnouncements = []
        futureAnnouncements = []
        for item in stockEventsAnnouncementsInst:
            if str(item.dateFrAnnouncement) > today:
                futureAnnouncements.append(EmployeeEncoder().encode(item))
            else:
                pastAnnouncements.append(EmployeeEncoder().encode(item))

        stockEventsLegalOrdersInst_list = []
        stockEventsLegalOrdersInst = stockEventsLegalOrders.objects.filter(stockProfileName=stock).order_by(
            '-exDateFrLegalOrders')
        if stockEventsLegalOrdersInst:
            for each in stockEventsLegalOrdersInst:
                stockEventsLegalOrdersInst_serial = stockEventsLegalOrdersSerializer(each)
                stockEventsLegalOrdersInst_list.append(stockEventsLegalOrdersInst_serial.data)

        # description field for SEO - starts
        try:
            stockEventsSEOInst = stockEventsSEO.objects.get(stockProfileName=stock)
            if stockEventsSEOInst:
                stockEventsSEOInst_ser = stockEventsSEOSerializer(stockEventsSEOInst)
                stockEventsSEOInst = stockEventsSEOInst_ser.data
        except:
            stockEventsSEOInst = None

        # description field for SEO - ends

        context = {
            'stock': stock_detail,
            'pastDividents': pastDividents,
            'futureDividents': futureDividents,
            'pastCorpActions': pastCorpActions,
            'futureCorpActions': futureCorpActions,
            'pastAnnouncements': pastAnnouncements,
            'futureAnnouncements': futureAnnouncements,
            'stockEventsLegalOrdersInst': stockEventsLegalOrdersInst_list,
            'stockAdmInst': stockAdmInst,
            'despositoryOptions': despositoryOptions,
            'saleType': saleType,
            'stockEventsSEOInst': stockEventsSEOInst,

        }
        return Response({'response': context})


@api_view(['GET'])
def ownershipViewapi(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    if request.method == 'GET':

        try:
            ownershipInst = stockOwnership.objects.get(stockProfileName=stock)
            if ownershipInst:
                ownershipInst_ser = stockOwnershipSerializer(ownershipInst)
                ownershipInst = ownershipInst_ser.data
        except:
            ownershipInst = None

        ownershipDirectorInst_list = []
        ownershipInstitutionalInst_list = []
        ownershipPatternInst_list = []

        ownershipDirectorInst = stockOwnershipDirector.objects.filter(stockProfileName=stock)
        if ownershipDirectorInst:
            for each in ownershipDirectorInst:
                ownershipDirectorInst_ser = stockOwnershipDirectorSerializer(each)
                ownershipDirectorInst_data = ownershipDirectorInst_ser.data
                ownershipDirectorInst_list.append(ownershipDirectorInst_data)

        ownershipInstitutionalInst = stockOwnershipInstitutional.objects.filter(stockProfileName=stock)
        if ownershipInstitutionalInst:
            for each in ownershipInstitutionalInst:
                ownershipInstitutionalInst_ser = stockOwnershipInstitutionalSerializer(each)
                ownershipInstitutionalInst_data = ownershipInstitutionalInst_ser.data
                ownershipInstitutionalInst_list.append(ownershipInstitutionalInst_data)
        ownershipPatternInst = stockOwnershipPattern.objects.filter(stockProfileName=stock).order_by('-year')
        if ownershipPatternInst:
            for each in ownershipPatternInst:
                ownershipPatternInst_ser = stockOwnershipPatternSerializer(each)
                ownershipPatternInst_data = ownershipPatternInst_ser.data
                ownershipPatternInst_list.append(ownershipPatternInst_data)

        totalPromoterholdingValue = mutualFundHoldingValue = domesticInstitutionalHoldingsValue = foreignInstitutionalHoldingsValue = others = institutionalHolding = publicInstitutionalHoldings = nonPublicInstitutionalHoldings = retail = employees = custodians = promoters = privatePublicInvestmenFirmVCs = False

        for item in ownershipPatternInst:
            if item.totalPromoterholdingValue:
                totalPromoterholdingValue = True
            if item.mutualFundHoldingValue:
                mutualFundHoldingValue = True
            if item.domesticInstitutionalHoldingsValue:
                domesticInstitutionalHoldingsValue = True
            if item.foreignInstitutionalHoldingsValue:
                foreignInstitutionalHoldingsValue = True
            if item.others:
                others = True
            if item.institutionalHolding:
                institutionalHolding = True
            if item.publicInstitutionalHoldings:
                publicInstitutionalHoldings = True
            if item.nonPublicInstitutionalHoldings:
                nonPublicInstitutionalHoldings = True
            if item.retail:
                retail = True
            if item.employees:
                employees = True
            if item.custodians:
                custodians = True
            if item.promoters:
                promoters = True
            if item.privatePublicInvestmenFirmVCs:
                privatePublicInvestmenFirmVCs = True

        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_ser = stockAdminSerializer(stockAdmInst)
                stockAdmInst = stockAdmInst_ser.data
        except:
            stockAdmInst = None
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        staticUrl = settings.STATIC_URL

        context = {
            'stock': stock_detail,
            'ownershipInst': ownershipInst,
            'ownershipDirectorInst': ownershipDirectorInst_list,
            'ownershipInstitutionalInst': ownershipInstitutionalInst_list,
            'ownershipPatternInst': ownershipPatternInst_list,
            'stockAdmInst': stockAdmInst,
            'despositoryOptions': despositoryOptions,
            'saleType': saleType,
            'staticUrl': staticUrl,
            'totalPromoterholdingValue': totalPromoterholdingValue,
            'mutualFundHoldingValue': mutualFundHoldingValue,
            'domesticInstitutionalHoldingsValue': domesticInstitutionalHoldingsValue,
            'foreignInstitutionalHoldingsValue': foreignInstitutionalHoldingsValue,
            'others': others,
            'institutionalHolding': institutionalHolding,
            'publicInstitutionalHoldings': publicInstitutionalHoldings,
            'nonPublicInstitutionalHoldings': nonPublicInstitutionalHoldings,
            'retail': retail,
            'employees': employees,
            'custodians': custodians,
            'promoters': promoters,
            'privatePublicInvestmenFirmVCs': privatePublicInvestmenFirmVCs,
        }
        return Response({'response': context})


@api_view(['GET'])
def newsViewapi(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    if request.method == 'GET':
        newsListRaw = {}
        websiteMasterInst = websiteMaster.objects.filter(stockProfileName=stock)
        websiteMasterInst_list = []
        if len(websiteMasterInst):
            for each in websiteMasterInst:
                websiteMasterInst_serial = websiteMasterSerializer(each)
                websiteMasterInst_list.append(websiteMasterInst_serial.data)

        pageType = request.GET.get('type')
        newsDatalist = []
        stockNewsInst_list = []
        newsArticles_list = []
        newsBlog_list = []
        newsVideoShorts_list = []
        newsVideos_list = []
        if pageType == 'articles-only':
            stockNewsInst = stockNews.objects.filter(stockProfileName=stock, newsType='Articles-Only').order_by(
                '-newsPublishDate')
            if len(stockNewsInst):
                for each in stockNewsInst:
                    stockNewsInst_serial = stockNewsSerializer(each)
                    stockNewsInst_list.append(stockNewsInst_serial.data)
            newsArticles = blogArticles.objects.filter(relatedResearchReports=stock).order_by('-dateForListing')
            if len(newsArticles):
                for each in newsArticles:
                    newsArticles_serial = blogArticlesSerializer(each)
                    newsArticles_list.append(newsArticles_serial.data)

            newsBlog = blogNews.objects.filter(relatedResearchReports=stock).order_by('-dateOfNews')
            if len(newsBlog):
                for each in newsBlog:
                    newsBlog_serial = blogNewsSerializer(each)
                    newsBlog_list.append(newsBlog_serial.data)
            for item in stockNewsInst:
                newsObj = newsClubbedObjects(item.title, item.newsPublishDate, item.source_self, item.get_current_image,
                                             item.get_absolute_url, item)
                newsDatalist.append(newsObj)
            for item in newsBlog:
                newsBlogObj = newsClubbedObjects(item.title, item.dateOfNews, 'News Blog', item.get_current_image,
                                                 item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(newsBlogObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsArticles:
                newsArticlesObj = newsClubbedObjects(item.title, item.dateForListing, 'Article Blog', item.articleImage,
                                                     item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(newsArticlesObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            with connections['cralwer'].cursor() as cursor:
                status = "'published'"
                SEOTitle = "'" + stock.seoTitle + "'"
                query = 'Select title, date, site, img, link from "crawlApp_googlenewsstore" where status=' + status + ' AND "connectedStock"=' + SEOTitle + ';'
                cursor.execute(query)
                newsListRaw = cursor.fetchall()
                for item in newsListRaw:
                    newsLink = 'https://' + str(item[4])
                    if item[3]:
                        imgLink = item[3]
                    else:
                        imgLink = stock.logo.url
                    crawledNewsSelf = newsClubbedObjects(item[0], item[1], item[2], imgLink, newsLink)
                    employeeJSONData = EmployeeEncoder().encode(crawledNewsSelf)
                    employeeJSON = json.loads(employeeJSONData)
                    newsDatalist.append(employeeJSON)
        elif pageType == 'videos-only':
            stockNewsInst = stockNews.objects.filter(stockProfileName=stock, newsType='Videos-Only').order_by(
                '-newsPublishDate')
            if len(stockNewsInst):
                for each in stockNewsInst:
                    stockNewsInst_serial = stockNewsSerializer(each)
                    stockNewsInst_list.append(stockNewsInst_serial.data)
            newsVideoShorts = blogVideosShorts.objects.filter(relatedResearchReports=stock).order_by('-releaseDate')
            if len(newsVideoShorts):
                for each in newsVideoShorts:
                    newsVideoShorts_serial = blogVideosShortsSerializer(each)
                    newsVideoShorts_list.append(newsVideoShorts_serial.data)
            newsVideos = blogVideos.objects.filter(relatedResearchReports=stock).order_by('-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideos_list.append(newsVideos_serial.data)
            for item in stockNewsInst:
                newsObj = newsClubbedObjects(item.title, item.newsPublishDate, item.source_self, item.get_current_image,
                                             item.get_absolute_url, item)
                employeeJSONData = EmployeeEncoder().encode(newsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsVideoShorts:
                if item.releaseDate:
                    itemDate = item.releaseDate.date()
                else:
                    itemDate = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d').date()
                shortsObj = newsClubbedObjects(item.title, itemDate, 'Shorts Blog', item.get_current_image,
                                               item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(shortsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsVideos:
                videosObj = newsClubbedObjects(item.title, item.releasedDate, 'Video Blog', item.get_current_image,
                                               item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(videosObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
        else:
            newsBlog = blogNews.objects.filter(relatedResearchReports=stock).order_by('-dateOfNews')
            if len(newsBlog):
                for each in newsBlog:
                    newsBlog_serial = blogNewsSerializer(each)
                    newsBlog_list.append(newsBlog_serial.data)
            newsVideoShorts = blogVideosShorts.objects.filter(relatedResearchReports=stock).order_by('-releaseDate')
            if len(newsVideoShorts):
                for each in newsVideoShorts:
                    newsVideoShorts_serial = blogVideosShortsSerializer(each)
                    newsVideoShorts_list.append(newsVideoShorts_serial.data)
            newsVideos = blogVideos.objects.filter(relatedResearchReports=stock).order_by('-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideos_list.append(newsVideos_serial.data)
            newsArticles = blogArticles.objects.filter(relatedResearchReports=stock).order_by('-dateForListing')
            if len(newsArticles):
                for each in newsArticles:
                    newsArticles_serial = blogArticlesSerializer(each)
                    newsArticles_list.append(newsArticles_serial.data)
            stockNewsInst = stockNews.objects.filter(stockProfileName=stock).order_by('-newsPublishDate')
            if len(stockNewsInst):
                for each in stockNewsInst:
                    stockNewsInst_serial = stockNewsSerializer(each)
                    stockNewsInst_list.append(stockNewsInst_serial.data)
            for item in stockNewsInst_list:
                newsObj = newsClubbedObjects(item.get('title'), item.get('newsPublishDate'), item.get('source_self'),
                                             item.get('get_current_image'), item.get('get_absolute_url'), item)
                employeeJSONData = EmployeeEncoder().encode(newsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsVideoShorts:
                if item.releaseDate:
                    itemDate = item.releaseDate.date()
                else:
                    itemDate = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d').date()
                shortsObj = newsClubbedObjects(item.title, itemDate, 'Shorts Blog', item.get_current_image,
                                               item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(shortsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)

            for item in newsBlog:
                newsBlogObj = newsClubbedObjects(item.title, item.dateOfNews, 'News Blog', item.get_current_image,
                                                 item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(newsBlogObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsVideos:
                videosObj = newsClubbedObjects(item.title, item.releasedDate, 'Video Blog', item.get_current_image,
                                               item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(videosObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsArticles:
                newsArticlesObj = newsClubbedObjects(item.title, item.dateForListing, 'Article Blog', item.articleImage,
                                                     item.get_absolute_url)
                employeeJSONData = EmployeeEncoder().encode(newsArticlesObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            with connections['cralwer'].cursor() as cursor:
                status = "'published'"
                SEOTitle = "'" + stock.seoTitle + "'"
                query = 'Select title, date, site, img, link from "crawlApp_googlenewsstore" where status=' + status + ' AND "connectedStock"=' + SEOTitle + ' order by date desc;'
                cursor.execute(query)
                newsListRaw = cursor.fetchall()
                for item in newsListRaw:
                    newsLink = 'https://' + str(item[4])
                    crawledNewsSelf = newsClubbedObjects(item[0], item[1], item[2], item[3], newsLink)
                    employeeJSONData = EmployeeEncoder().encode(crawledNewsSelf)
                    employeeJSON = json.loads(employeeJSONData)
                    newsDatalist.append(employeeJSON)
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_ser = stockAdminSerializer(stockAdmInst)
                stockAdmInst = stockAdmInst_ser.data
        except:
            stockAdmInst = None
        despositoryOptions, saleType = rightSideMenuObjs_serialized()

        # newsDatalist.sort(key=lambda x: x.releaseDate_self, reverse=True)

        # description field for SEO - starts
        stockNewsSEOInst_dict = {}
        try:
            stockNewsSEOInst = stockNewsSEO.objects.get(stockProfileName=stock)
            if stockNewsSEOInst:
                serializer = stockNewsSEOSerializer(stockNewsSEOInst)
                stockNewsSEOInst_dict.update(serializer.data)

        except:
            stockNewsSEOInst = None
        # description field for SEO - ends

        context = {
            'stock': stock_detail,
            'stockNewsInst': stockNewsInst_list,
            'websiteMasterInst': websiteMasterInst_list,
            'stockAdmInst': stockAdmInst,
            'despositoryOptions': despositoryOptions,
            'saleType': saleType,
            'newsDatalist': newsDatalist,
            'newsListRaw': newsListRaw,
            'stockNewsSEOInst': stockNewsSEOInst
        }
        return Response({'response': context})


@api_view(['POST'])
def stockadmin(request, slug):
    if request.method == 'POST':
        stock = get_object_or_404(stockBasicDetail, id=slug)

        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            print("stockAdmInst", stockAdmInst)
        except:
            stockAdmInst = None
        stockadminserializer = StockAdminSerializer(stockAdmInst, request.data, partial=True)
        if stockadminserializer.is_valid():
            stockadminserializer.save()
            return Response({'response': stockadminserializer.data})
        else:
            return Response({'response': stockadminserializer.errors})


@api_view(['GET'])
def getfaqview(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)

    if stock.status == 'draft' and not request.user.is_staff:
        return Response({'response': 'websiteApp:buypreIPOUrl'})
    if request.method == 'GET':
        researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
        researchReportFAQsInst_list = []
        if len(researchReportFAQsInst):
            for each in researchReportFAQsInst:
                researchReportFAQs_serial = researchReportFAQsSerializer(each)
                data = researchReportFAQs_serial.data
                data['questions'] = data['questions'].replace('stock_name_auto', stock.stockName)
                data['answers'] = data['answers'].replace('stock_name_auto', stock.stockName)
                researchReportFAQsInst_list.append(data)

        commonFAQInst = commonFAQ.objects.all().order_by('id')
        commonFAQInst_list = []
        if len(commonFAQInst):
            for each in commonFAQInst:
                commonFAQInst_serial = commonFAQSerializer(each)
                data = commonFAQInst_serial.data
                data['questions'] = data['questions'].replace('stock_name_auto', stock.stockName)
                data['answers'] = data['answers'].replace('stock_name_auto', stock.stockName)
                commonFAQInst_list.append(data)
        response_dict = {"commonFAQInst": commonFAQInst_list, "researchReportFAQsInst": researchReportFAQsInst_list}
        return Response({'response': response_dict})


@api_view(['GET'])
def getsnapshotview(request, slug):
    if request.method == 'GET':
        response_dict = {}
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = ""
        if stock:
            stock_detail = StockSerializer(stock)
            stock_detail = stock_detail.data

        if stock.status == 'draft' and not request.user.is_staff:
            return Response({'response': 'websiteApp:buypreIPOUrl'})

        renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
        if renderBankNBFCsTemplates:
            return redirect('stockApp:banknbfcViewapi', slug)

        currentPrice = localOrScreenerPriceView(stock)
        print("current price", currentPrice)
        callingFunction = 'snapshot'

        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                #	for each in stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
            print("stockAdmInst", stockAdmInst)
        except:
            stockAdmInst = None
        # stockAdmInst_list = []
        essentialInst_list = []
        essentialInst_detail = ""
        try:
            essentialInst = stockEssentials.objects.get(stockProfileName=stock)
            if essentialInst:
                #	for each in stockAdmInst:
                essentialInst_detail = stockEssentialsSerializer(essentialInst)
                essentialInst_detail = essentialInst_detail.data
        except:
            essentialInst = None
            essentialInst_list = None
            essentialInst_detail = ""
        stock_detail["stockProfileNameSE"] = essentialInst_detail
        financialFigureUnitsInst_detail = ""
        try:
            financialFigureUnitsInst = financialFigureUnits.objects.get(stockProfileName=stock)
            if financialFigureUnitsInst:
                financialFigureUnitsInst_detail = financialFigureUnitsSerializer(essentialInst)
                financialFigureUnitsInst_detail = financialFigureUnitsInst_detail.data
        except:
            financialFigureUnitsInst = None
            financialFigureUnitsInst_detail = ""

        stock_detail["stockProfileNameFFU"] = financialFigureUnitsInst_detail

        stockInvestmentChecklistInst_detail = ""
        try:
            stockInvestmentChecklistInst = stockInvestmentChecklist.objects.get(stockProfileName=stock)
            if stockInvestmentChecklistInst:
                #	for each in stockInvestmentChecklistInst:
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistSerializer(stockInvestmentChecklistInst)
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistInst_detail.data
        except:
            stockInvestmentChecklistInst_list = None

        stock_detail["stockProfileNameSIC"] = stockInvestmentChecklistInst_detail

        stockIPOInst_details = ""
        try:
            stockIPOInst = stockIPO.objects.get(stockProfileName=stock)
            if stockIPOInst:
                #	for each in stockIPOInst:
                stockIPOInst_details = stockIPOSerializer(stockIPOInst)
                stockIPOInst_details = stockIPOInst_details.data
        except:
            stockIPOInst = None

        stock_detail["stockProfileNameSI"] = stockIPOInst_details

        stockDetailsInst_details = ""
        try:
            stockDetailsInst = stockDetails.objects.get(stockProfileName=stock)
            if stockDetailsInst:
                #	for each in stockDetailsInst:
                stockDetailsInst_details = stockDetailsSerializer(stockDetailsInst)
                stockDetailsInst_details = stockDetailsInst_details.data
        except:
            stockDetailsInst = None

        stock_detail["stockProfileNameSD"] = stockDetailsInst_details

        stockFundingRoundsInst_list = []
        try:
            stockFundingRoundsInst = stockFundingRounds.objects.filter(stockProfileName=stock).order_by(
                '-dateOfInvestment')
            if stockFundingRoundsInst:
                for each in stockFundingRoundsInst:
                    stockFundingRoundsInst_ser = stockFundingRoundsSerializer(each)
                    stockFundingRoundsInst_list.append(stockFundingRoundsInst_ser.data)
        except:
            stockFundingInst = None

        stockFundingInst_detail = ""
        try:
            stockFundingInst = stockFunding.objects.get(stockProfileName=stock)
            if stockFundingInst:
                #	for each in stockFundingInst:
                stockFundingInst_detail = stockFundingSerializer(stockFundingInst)
                stockFundingInst_detail = stockFundingInst_detail.data
        except:
            stockFundingInst = None

        stock_detail['stockProfileNameSF'] = stockFundingInst_detail

        try:
            promotorHolding = stockOwnershipPattern.objects.get(stockProfileName=stock, year=currentYear)
            promotorHolding = promotorHolding.totalPromoterholdingValue
        except:
            promotorHolding = None
        try:
            latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
            totalRevCY = latestProfitAndLoss.totalRevenue
            patCY = latestProfitAndLoss.netIncome
            epsCY = latestProfitAndLoss.basicEPS
            dps = latestProfitAndLoss.DPS
        except:
            totalRevCY = None
            patCY = None
            epsCY = None
            dps = None
        try:
            latestCashFlow = stockCashFlow.objects.filter(stockProfileName=stock).latest('year')
            cashFlowOperationsCY = latestCashFlow.cashFromOperatingActivities
            cashFlowFinancingCY = latestCashFlow.cashFromFinancingActivities
        except:
            cashFlowOperationsCY = None
            cashFlowFinancingCY = None

        categoryForEss = categoryOptions.objects.all().order_by('name')
        categoryForEss_list = []
        if categoryForEss:
            for each in categoryForEss:
                categoryForEss = categoryOptionsSerializer(each)
                categoryForEss_list.append(categoryForEss.data)
        sectorForEss = sectorOptions.objects.all().order_by('name')
        sectorForEss_list = []
        if sectorForEss:
            for each in sectorForEss:
                categoryForEss = sectorOptionsSerializer(each)
                sectorForEss_list.append(categoryForEss.data)
        subSectorForEss = subSectorOptions.objects.all().order_by('name')
        subSectorForEss_list = []
        if subSectorForEss:
            for each in subSectorForEss:
                subSectorForEss = subSectorOptionsSerializer(each)
                subSectorForEss_list.append(subSectorForEss.data)
        revenueBreakupInst = stockRevenueBreakUp.objects.filter(stockProfileName=stock)
        revenueBreakupInst_list = []
        if revenueBreakupInst:
            for each in revenueBreakupInst:
                revenueBreakupInst_ser = stockRevenueBreakUpSerializer(each)
                revenueBreakupInst_list.append(revenueBreakupInst_ser.data)
        benGrahamOrDCFInst_detail = ""
        try:
            benGrahamOrDCFInst = benGrahamOrDCF.objects.get(stockProfileName=stock)
            if benGrahamOrDCFInst:
                #	for each in benGrahamOrDCFInst:
                benGrahamOrDCFInst_detail = benGrahamOrDCFSerializer(benGrahamOrDCFInst)
                benGrahamOrDCFInst_detail = benGrahamOrDCFInst_detail.data
        except:
            benGrahamOrDCFInst = None
        returnedGrowthROEVal = ROEgrowthCalculator(stock)
        response_dict.update({"returnedGrowthROEVal": returnedGrowthROEVal})
        # return returnedGrowthROEVal
        intrinsicVal = intrinsicFormula(stock)
        response_dict.update({"intrinsicVal": intrinsicVal})
        returnedRevenueGrowthAlgoProgrammedData, processedNetProfitGrowthTextual = calGrowthTemplateDataView(stock,
                                                                                                             requestFrom='snapshot')
        compoundSalesGrowth = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
        # compoundProfitGrowth = calculateProgrammedGrowth(processedNetProfitGrowthTextual)
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        stockTransferDepositoryOptions_list = []
        try:
            if despositoryOptions:
                for each in despositoryOptions:
                    stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                    stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
        except:
            despositoryOptions = None
            stockTransferDepositoryOptions_list = []
        saleTypeOptions_list = []
        try:
            if saleType:
                for each in saleType:
                    saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                    saleTypeOptions_list.append(saleTypeOptions_ser.data)
        except:
            saleType = None
            saleTypeOptions_list = []

        profitAndLossQuerySet = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('-year')
        revenueGrowth = calculateGrowthNew(profitAndLossQuerySet, 'revenue')
        compoundProfitGrowth = calculateGrowthNew(profitAndLossQuerySet, 'netIncome')
        try:
            bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
            bookValYear = bookValues.year
            totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=bookValYear)
            bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
        except:
            bookValues = bookValueCal = None
        fundingRoundsUnitInst_detail = ""
        try:
            fundingRoundsUnitInst = get_object_or_404(foundingRoundsFigureUnits, stockProfileName=stock)
            if fundingRoundsUnitInst:
                fundingRoundsUnitInst_detail = foundingRoundsFigureUnitsSerializer(fundingRoundsUnitInst)
                fundingRoundsUnitInst_detail = fundingRoundsUnitInst_detail.data
        except:
            fundingRoundsUnitInst = None
            fundingRoundsUnitInst_detail = ""

        fundingDetailsVisibilityInst_detail = ""
        try:
            fundingDetailsVisibilityInst = get_object_or_404(fundingDetailsVisibility, stockProfileName=stock)
            if fundingDetailsVisibilityInst:
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilitySerializer(fundingDetailsVisibilityInst)
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilityInst_detail.data
        except:
            fundingDetailsVisibilityInst = None
            fundingDetailsVisibilityInst_detail = ""

        stock_detail['stockProfileNameFDVI'] = fundingDetailsVisibilityInst_detail

        if essentialInst:
            totalSharesInst = essentialInst.totalShares
        else:
            totalSharesInst = 0

        try:
            stockProfitAndLossInst = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
            basicEps = stockProfitAndLossInst.basicEPS
            dilutedEps = stockProfitAndLossInst.dilutedEPS
        except:
            basicEps = 1
            dilutedEps = 1

        eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
        try:
            PEvalue = round((currentPrice / eps), 2)
        except:
            PEvalue = None

        if bookValues:
            bookVal = bookValueCal
        else:
            bookVal = 1
        try:
            PBvalue = round((currentPrice / bookVal), 2)
        except:
            PBvalue = None

        try:
            earningsYield = round((epsCY / currentPrice) * 100, 2)
        except:
            earningsYield = None

        try:
            dividendYield = round((dps / currentPrice) * 100, 2)
        except:
            dividendYield = None

        # enterprise value
        cashAndShortTermEqui = minorityInt = 0
        try:
            stockBalanceSheetLatestObj = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
            cashAndShortTermEqui = stockBalanceSheetLatestObj.cashAndShortTermInvestments
            minorityInt = stockBalanceSheetLatestObj.minorityInterest
        except:
            pass
        balWithRBI = prefEquity = 0
        try:
            balWithRBI = essentialInst.balance_with_RBI
            prefEquity = essentialInst.preference_equity
        except:
            pass

        if not balWithRBI:
            balWithRBI = 0
        if not prefEquity:
            prefEquity = 0
        totalLngDebt = currPortLngTermDebt = currPortionLeases = lngTermPortionOfLeases = 0
        try:
            latestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
            if latestBalanceSheet.totalLongTermDebt:
                totalLngDebt = Decimal(latestBalanceSheet.totalLongTermDebt)
            if latestBalanceSheet.currentPortionOfLongTermDebt:
                currPortLngTermDebt = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
            if latestBalanceSheet.currentPortionOfLeases:
                currPortionLeases = Decimal(latestBalanceSheet.currentPortionOfLeases)
            if latestBalanceSheet.longTermPortionOfLeases:
                lngTermPortionOfLeases = Decimal(latestBalanceSheet.longTermPortionOfLeases)
        except:
            pass
        totalDebt = totalLngDebt + currPortionLeases + lngTermPortionOfLeases + currPortLngTermDebt
        try:
            marketCap = (totalSharesInst * currentPrice) / 10000000
            marketCapForEnterprise = marketCap
        except:
            marketCap = None
            marketCapForEnterprise = None
        try:
            marketCapForEnterprise = numberConversion(marketCapForEnterprise, currentSystem='Cr',
                                                      convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        enterpriseVal = returnDecimalOrZero(marketCapForEnterprise) - (
                returnDecimalOrZero(cashAndShortTermEqui) - returnDecimalOrZero(balWithRBI)) + returnDecimalOrZero(
            totalDebt) + returnDecimalOrZero(prefEquity) + returnDecimalOrZero(minorityInt)
        try:
            enterpriseVal = numberConversion(enterpriseVal, currentSystem=stock.stockProfileNameFFU.financialNumbers,
                                             convertTo='Cr')
        except:
            pass

        researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
        researchReportFAQsInst_list = []
        if len(researchReportFAQsInst):
            for each in researchReportFAQsInst:
                researchReportFAQs_serial = researchReportFAQsSerializer(each)
                researchReportFAQsInst_list.append(researchReportFAQs_serial.data)

        totalShareYearlyDataInst = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                       shareType='financial_year').order_by('year')
        totalShareYearlyDataInst_list = []
        if len(totalShareYearlyDataInst):
            for each in totalShareYearlyDataInst:
                totalShareYearly_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInst_list.append(totalShareYearly_serial.data)

        totalShareYearlyDataInstConvertible = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                                  shareType='convertible_equity').order_by(
            'year')
        totalShareYearlyDataInstConvertible_list = []
        if len(totalShareYearlyDataInstConvertible):
            for each in totalShareYearlyDataInstConvertible:
                totalShareYearlyData_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInstConvertible_list.append(totalShareYearlyData_serial.data)

        commonFAQInst = commonFAQ.objects.all().order_by('id')
        commonFAQInst_list = []
        if len(commonFAQInst):
            for each in commonFAQInst:
                commonFAQInst_serial = commonFAQSerializer(each)
                commonFAQInst_list.append(commonFAQInst_serial.data)

        response_dict.update({  # "essentialInst": essentialInst_detail,
            "stock": stock_detail,
            "stockFundingRoundsInst": stockFundingRoundsInst_list,
            "returnedRevenueGrowthAlgoProgrammedData": returnedRevenueGrowthAlgoProgrammedData,
            "processedNetProfitGrowthTextual": processedNetProfitGrowthTextual,
            "compoundSalesGrowth": compoundSalesGrowth,
            "despositoryOptions": despositoryOptions,
            "saleType": saleType,
            "revenueGrowth": revenueGrowth,
            "compoundProfitGrowth": compoundProfitGrowth,
            "bookValueCal": bookValueCal,
            "fundingRoundsUnitInst": fundingRoundsUnitInst_detail,
            # "fundingDetailsVisibilityInst": fundingDetailsVisibilityInst_detail,
            "enterpriseVal": enterpriseVal,
            "PEvalue": PEvalue,
            "PBvalue": PBvalue,
            "earningsYield": earningsYield,
            "dividendYield": dividendYield,
            "researchReportFAQsInst": researchReportFAQsInst_list,
            "totalShareYearlyDataInst": totalShareYearlyDataInst_list,
            "totalShareYearlyDataInstConvertible": totalShareYearlyDataInstConvertible_list,
            "commonFAQInst": commonFAQInst_list,
            "cashFlowOperationsCY": cashFlowOperationsCY,
            "cashFlowFinancingCY": cashFlowFinancingCY,
            "promotorHolding": promotorHolding,
            "totalRevCY": totalRevCY,
            "patCY": patCY,
            "marketCap": marketCap,
            "stockAdmInst": stockAdmInst_detail,
            # "stockInvestmentChecklistInst": stockInvestmentChecklistInst_list,
            "categoryForEss": categoryForEss_list,
            "sectorForEss": sectorForEss_list,
            "subSectorForEss": subSectorForEss_list,
            # "stockIPOInst": stockIPOInst_list,
            # "stockDetailsInst": stockDetailsInst_list,
            "epsCY": epsCY,
            "returnedGrowthROEVal": returnedGrowthROEVal,
            "intrinsicVal": intrinsicVal,
            "benGrahamOrDCFInst": benGrahamOrDCFInst_detail,
            "revenueBreakupInst": revenueBreakupInst_list})
        return Response({'response': response_dict})


#
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


#
def adsenseTextView(request):
    file_data = "google.com, pub-5016336417243730, DIRECT, f08c47fec0942fa0"
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ads.txt"'
    return response


#
def siteMapGenerator(sender, instance, created, **kwargs):
    postStatus = instance.status
    # keyratio
    try:
        keyRatioObj = get_object_or_404(keyratioUrlsForSitemap, stockProfileName=instance)
        keyRatioObj.status = postStatus
        keyRatioObj.save()
    except:
        try:
            keyratioUrlsForSitemap.objects.create(stockProfileName=instance, status=postStatus)
        except:
            messages.error(request, 'Site Map for Key Ratio not updated, Pls try again.')
    # // keyratio
    # peers
    try:
        peersObj = get_object_or_404(peersUrlsForSitemap, stockProfileName=instance)
        peersObj.status = postStatus
        peersObj.save()
    except:
        try:
            peersUrlsForSitemap.objects.create(stockProfileName=instance, status=postStatus)
        except:
            messages.error(request, 'Site Map for Peers not updated, Pls try again.')
    # // peers
    # financial
    try:
        peersObj = get_object_or_404(financialUrlsForSitemap, stockProfileName=instance)
        peersObj.status = postStatus
        peersObj.save()
    except:
        try:
            financialUrlsForSitemap.objects.create(stockProfileName=instance, status=postStatus)
        except:
            messages.error(request, 'Site Map for Peers not updated, Pls try again.')
    # // financial
    # ownership
    try:
        peersObj = get_object_or_404(ownershipUrlsForSitemap, stockProfileName=instance)
        peersObj.status = postStatus
        peersObj.save()
    except:
        try:
            ownershipUrlsForSitemap.objects.create(stockProfileName=instance, status=postStatus)
        except:
            messages.error(request, 'Site Map for Peers not updated, Pls try again.')
    # // ownership
    # news
    try:
        peersObj = get_object_or_404(newsUrlsForSitemap, stockProfileName=instance)
        peersObj.status = postStatus
        peersObj.save()
    except:
        try:
            newsUrlsForSitemap.objects.create(stockProfileName=instance, status=postStatus)
        except:
            messages.error(request, 'Site Map for Peers not updated, Pls try again.')
    # // news
    # events
    try:
        peersObj = get_object_or_404(eventsUrlsForSitemap, stockProfileName=instance)
        peersObj.status = postStatus
        peersObj.save()
    except:
        try:
            eventsUrlsForSitemap.objects.create(stockProfileName=instance, status=postStatus)
        except:
            messages.error(request, 'Site Map for Peers not updated, Pls try again.')


# // events


post_save.connect(siteMapGenerator, sender=stockBasicDetail)


#
def renderBankNBFCsTemplatesView(stock):
    renderBankNBFC = False
    try:
        templateChecker = stockEssentials.objects.get(stockProfileName=stock)
    except:
        templateChecker = None
    if templateChecker:
        if templateChecker.subSector:
            subsector = templateChecker.subSector.name.lower()
            if subsector == 'consumer finance'.lower() or \
                    subsector == 'housing finance'.lower() or \
                    subsector == 'ASSET MANAGEMENT'.lower() or \
                    subsector == 'SPECIALIZED FINANCE'.lower() or \
                    subsector == 'PRIVATE BANKS'.lower() or \
                    subsector == 'PUBLIC BANKS'.lower() or \
                    subsector == 'SMALL FINANCE BANK'.lower() or \
                    subsector == 'Stock Broking'.lower() or \
                    subsector == 'DIVERSIFIED FINANCIALS'.lower():
                renderBankNBFC = True
    return renderBankNBFC


#
def brokenLinkHandler(request):
    redirectQuerySet = redirectBucket.objects.all()
    pathRequest = request.get_full_path()
    for item in redirectQuerySet:
        if item.source == pathRequest:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = None
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            createCountObj = redirectCount(redirectInst=item, clientIP=ip)
            createCountObj.save()
            return item.destination
    return False


#
def handler404(request, exception):
    redireccTo = brokenLinkHandler(request)
    if redireccTo:
        return HttpResponseRedirect(redireccTo)
    return redirect('render404PageUrl')


#
def render404Page(request):
    return render(request, '404.html', status=404)


#
def handler500(request, exception, template_name="500.html"):
    response = render_to_response(template_name)
    response.status_code = 500
    return response


#
def rightSideMenuObjs_serialized():
    despositoryOptions = stockTransferDepositoryOptions.objects.all()
    despositoryOptions_list = []
    if despositoryOptions:
        for each in despositoryOptions:
            subSectorForEss_serial = subSectorOptionsSerializer(each)
            despositoryOptions_list.append(subSectorForEss_serial.data)
    saleType = saleTypeOptions.objects.all()
    saleType_list = []
    if saleType:
        for each in saleType:
            saleType_serial = saleTypeOptionsSerializer(each)
            saleType_list.append(saleType_serial.data)
    return despositoryOptions_list, saleType_list


#
def rightSideMenuObjs():
    despositoryOptions = stockTransferDepositoryOptions.objects.all()
    saleType = saleTypeOptions.objects.all()
    return despositoryOptions, saleType


#
def orderDict(passedDict):
    sortedPassedDict = dict(sorted(passedDict.items(), key=operator.itemgetter(1), reverse=True))
    return sortedPassedDict


#
def return_val_or_0(value):
    if value:
        return value
    else:
        value = 0
        return value


#
def return_val_or_1(value):
    if value:
        return value
    else:
        value = 1
        return value


#
def return_number_or_0(value):
    if type(value) == int or type(value) == float:
        return value
    else:
        value = 0
    return value


#
def return_number_or_1(value):
    if type(value) == int or type(value) == float:
        return value
    else:
        value = 1
    return value


#
def return_decimal_or_0(value):
    if type(value) == Decimal:
        return value
    else:
        value = 0
    return value


#
def convert_to_decimal(value):
    if value:
        return Decimal(value)
    else:
        return Decimal(0)


#
def check_eps_basic_or_diluted(eps, dilutedEps):
    if eps:
        returnVal = eps
    elif dilutedEps:
        returnVal = dilutedEps
    else:
        returnVal = False
    return returnVal


#
def leadLandingView(request):
    return render(request, 'UI/leadLanding.html')



#
# def calGrowthFormulaView(CYval=0.00, PYval=0.00, years=1.00):
# 	if CYval == None or PYval == None:
# 		return False
# 	elif CYval < 0 or PYval < 0:
# 		calVal = 'negative'
# 		return calVal
# 	else:
# 		if PYval == 0:
# 			PYval = 1
# 		dividedVal = CYval / PYval
# 		powerVal = 1 / years
# 		poweredVal = pow(float(dividedVal), float(powerVal))
# 		calVal = (poweredVal - 1) * 100
# 		return calVal

def calGrowthFormulaView(CYval=0.00, PYval=0.00, years=1.00):
	# print(f"Cy val: {CYval} and PYcal: {PYval} and years: {years}")
	tempNegHand = 1
	if CYval == None or PYval == None:
		return False
	elif CYval > 0 and PYval < 0:
		PYval = (-1)* PYval
		tempNegHand = 1
	elif CYval < 0 and PYval > 0:
		CYval = (-1)* CYval
		tempNegHand = -1
	elif CYval < 0 and PYval < 0:
		CYval = (-1)* CYval
		PYval = (-1)* PYval
		tempNegHand = -1
	else:
		if PYval == 0:
			PYval = 1
	dividedVal = CYval / PYval
	powerVal = 1 / years
	poweredVal = pow(float(dividedVal), float(powerVal))
	calVal = (poweredVal - 1) * 100
	return (calVal*tempNegHand)


#
def calculateGrowthNew(querySetForGrowth, growthKey):
    lengthOfQuerySet = 0
    if querySetForGrowth:
        lengthOfQuerySet = querySetForGrowth.count()
    calculatedGrowth = {}
    if lengthOfQuerySet > 1 and lengthOfQuerySet <= 3:
        i = 0
        for item in querySetForGrowth:
            CYYear = item.year
            if i == 0:
                if growthKey == 'totalRevenue':
                    CYval = item.totalRevenue
                elif growthKey == 'revenue':
                    CYval = item.revenue
                elif growthKey == 'netIncome':
                    CYval = item.netIncome
            try:
                PYObj = querySetForGrowth.get(year=CYYear - 1)
                if growthKey == 'totalRevenue':
                    PYval = PYObj.totalRevenue
                elif growthKey == 'revenue':
                    PYval = PYObj.revenue
                elif growthKey == 'netIncome':
                    PYval = PYObj.netIncome
            except:
                PYval = None
            i += 1
            if PYval and CYval:
                growth = calGrowthFormulaView(CYval, PYval, i)
                calculatedGrowth[i] = growth
    elif lengthOfQuerySet >= 4:
        CYval = PYval = None
        firstElem = querySetForGrowth.first()
        lastElem = querySetForGrowth.last()
        if growthKey == 'totalRevenue':
            CYval = firstElem.totalRevenue
        elif growthKey == 'revenue':
            CYval = firstElem.revenue
        elif growthKey == 'netIncome':
            CYval = firstElem.netIncome
        CYYear = firstElem.year
        try:
            PYObj = querySetForGrowth.get(year=CYYear - 1)
            if growthKey == 'totalRevenue':
                PYval = PYObj.totalRevenue
            elif growthKey == 'revenue':
                PYval = PYObj.revenue
            elif growthKey == 'netIncome':
                PYval = PYObj.netIncome
        except:
            pass
        if CYval and PYval:
            growth = calGrowthFormulaView(CYval, PYval, 1)
            calculatedGrowth[1] = growth
        PYval = None
        checkBest1 = lengthOfQuerySet // 2
        midYearObjs = querySetForGrowth[checkBest1:checkBest1 + 1]
        evenNum = True
        if (lengthOfQuerySet % 2) == 0:
            evenNum = False
        for item in midYearObjs:
            midYearObjYear = item.year
            if growthKey == 'totalRevenue':
                PYval = item.totalRevenue
            elif growthKey == 'revenue':
                PYval = item.revenue
            elif growthKey == 'netIncome':
                PYval = item.netIncome
        growth1 = calGrowthFormulaView(CYval, PYval, checkBest1)
        growth2 = None
        if evenNum:
            try:
                PYObj = querySetForGrowth.get(year=midYearObjYear - 1)
                if growthKey == 'totalRevenue':
                    PYval = PYObj.totalRevenue
                elif growthKey == 'revenue':
                    PYval = PYObj.revenue
                elif growthKey == 'netIncome':
                    PYval = PYObj.netIncome
                midYearObjYearForEven = item.year
            except:
                PYval = None
            if CYval and PYval:
                growth2 = calGrowthFormulaView(CYval, PYval, checkBest1 + 1)
        try:
            DecimalGrowth1 = Decimal(growth1)
        except:
            DecimalGrowth1 = None
        try:
            DecimalGrowth2 = Decimal(growth2)
        except:
            DecimalGrowth2 = None
        if DecimalGrowth1 and DecimalGrowth2:
            if DecimalGrowth1 > DecimalGrowth2:
                calculatedGrowth[checkBest1] = growth1
            else:
                calculatedGrowth[checkBest1 + 1] = growth2
        elif DecimalGrowth1 and not DecimalGrowth2:
            calculatedGrowth[checkBest1] = growth1
        elif not DecimalGrowth2 == None:
            calculatedGrowth[checkBest1 + 1] = growth2
        PYval = None
        try:
            CYYear = lastElem.year + 1
            if growthKey == 'totalRevenue':
                PYval = lastElem.totalRevenue
            elif growthKey == 'revenue':
                PYval = lastElem.revenue
            elif growthKey == 'netIncome':
                PYval = lastElem.netIncome
        except:
            pass
        if CYval and PYval:
            growth = calGrowthFormulaView(CYval, PYval, lengthOfQuerySet - 1)
            calculatedGrowth[lengthOfQuerySet - 1] = growth
    return (calculatedGrowth)


#
def calculateForListGrowthNew(objList, growthKey):
    listLength = 0
    if objList:
        listLength = len(objList)
    calculatedGrowth = {}
    if listLength > 1 and listLength <= 3:
        i = 0
        for item in objList:
            CYYear = item.year
            if i == 0:
                if growthKey == 'roe':
                    CYval = item.value
            try:
                PYObj = objList[i + 1]
                if growthKey == 'roe':
                    PYval = PYObj.value
            except:
                PYval = None
            i += 1
            if PYval and CYval:
                growth = calGrowthFormulaView(CYval, PYval, i)
                calculatedGrowth[i] = growth
    elif listLength >= 4:
        CYval = PYval = None
        firstElem = objList[0]
        lastElem = objList[-1]
        if growthKey == 'roe':
            CYval = firstElem.value
        CYYear = firstElem.year
        try:
            PYObj = objList[1]
            if growthKey == 'roe':
                PYval = PYObj.value
        except:
            pass
        if CYval and PYval:
            growth = calGrowthFormulaView(CYval, PYval, 1)
            calculatedGrowth[1] = growth
        PYval = None

        checkBest1 = listLength // 2
        midYearObjs = objList[checkBest1:checkBest1 + 1]
        evenNum = False
        if (listLength % 2) == 0:
            evenNum = True
        for item in midYearObjs:
            midYear = item.year
            if growthKey == 'roe':
                PYval = item.value
        growth1 = calGrowthFormulaView(CYval, PYval, checkBest1)
        growth2 = None
        if evenNum:
            try:
                PYObj = objList.get(year=midYear - 1)
                if growthKey == 'roe':
                    PYval = PYObj.value
            except:
                PYval = None
            if CYval and PYval:
                growth2 = calGrowthFormulaView(CYval, PYval, checkBest1 + 1)

        try:
            DecimalGrowth1 = Decimal(growth1)
        except:
            DecimalGrowth1 = None
        try:
            DecimalGrowth2 = Decimal(growth2)
        except:
            DecimalGrowth2 = None
        if DecimalGrowth1 and DecimalGrowth2:
            if DecimalGrowth1 > DecimalGrowth2:
                calculatedGrowth[checkBest1] = growth1
            else:
                calculatedGrowth[checkBest1 + 1] = growth2
        elif DecimalGrowth1 and not DecimalGrowth2:
            calculatedGrowth[checkBest1] = growth1
        elif not DecimalGrowth2 == None:
            calculatedGrowth[checkBest1 + 1] = growth2
        PYval = None
        try:
            CYYear = lastElem.year + 1
            CYObj = objList[-2]
            if growthKey == 'roe':
                # CYval = CYObj.value
                PYval = lastElem.value
        except:
            pass
        if CYval and PYval:
            growth = calGrowthFormulaView(CYval, PYval, listLength - 1)
            calculatedGrowth[listLength - 1] = growth
    return (calculatedGrowth)


# for roe only

def calculateForListGrowthNewRoe(objList, growthKey):
    listLength = 0
    if objList:
        listLength = len(objList)
    calculatedGrowth = {}
    print(listLength)
    if listLength >= 1 and listLength <= 3:
        for item in objList:
            calculatedGrowth[item.year] = item.value

    elif listLength >= 4:

        CYval = PYval = None
        firstElem = objList[0]
        lastElem = objList[-1]
        if growthKey == 'roe':
            CYval = firstElem.value
        CYYear = firstElem.year
        try:
            PYObj = objList[1]
            if growthKey == 'roe':
                PYval = PYObj.value
        except:
            pass
        if CYval and PYval:
            calculatedGrowth[firstElem.year] = CYval
            pass
        PYval = None

        checkBest1 = listLength // 2
        midYearObjs = objList[checkBest1:checkBest1 + 1]
        evenNum = False
        if (listLength % 2) == 0:
            evenNum = True

        print(evenNum)
        for item in midYearObjs:
            midYear = item.year
            if growthKey == 'roe':
                PYval = item.value
        growth1 = PYval
        growth2 = None
        if evenNum:
            PYObj = objList[checkBest1 - 1]
            print(PYObj.year)
            if growthKey == 'roe':
                PYval = PYObj.value

            if CYval and PYval:
                growth2 = PYval
        try:
            DecimalGrowth1 = Decimal(growth1)
        except:
            DecimalGrowth1 = None
        try:
            DecimalGrowth2 = Decimal(growth2)
        except:
            DecimalGrowth2 = None

        if DecimalGrowth1 and DecimalGrowth2:
            if DecimalGrowth1 > DecimalGrowth2:
                calculatedGrowth[midYear] = growth1
            else:
                calculatedGrowth[midYear + 1] = growth2

        elif DecimalGrowth1 and not DecimalGrowth2:
            calculatedGrowth[midYear] = growth1
        elif not DecimalGrowth2 == None:
            calculatedGrowth[midYear + 1] = growth2

        PYval = None
        try:
            CYYear = lastElem.year + 1
            CYObj = objList[-2]
            if growthKey == 'roe':
                PYval = lastElem.value
        except:
            pass
        if CYval and PYval:
            calculatedGrowth[lastElem.year] = PYval
    return (calculatedGrowth)


#
# def calculateGrowthNew(querySetForGrowth, growthKey):
# 	lengthOfQuerySet = 0
# 	if querySetForGrowth:
# 		lengthOfQuerySet = querySetForGrowth.count() - 1
# 	calculatedGrowth = {}
# 	if lengthOfQuerySet >= 1 and lengthOfQuerySet < 4:
# 		i = 0
# 		for item in querySetForGrowth:
# 			CYYear = item.year
# 			if i == 0:
# 				if growthKey == 'totalRevenue':
# 					CYval = item.totalRevenue
# 				elif growthKey == 'revenue':
# 					CYval = item.revenue
# 				elif growthKey == 'netIncome':
# 					CYval = item.netIncome
# 			try:
# 				PYObj = querySetForGrowth.get(year = CYYear - 1)
# 				if growthKey == 'totalRevenue':
# 					PYval = PYObj.totalRevenue
# 				elif growthKey == 'revenue':
# 					PYval = PYObj.revenue
# 				elif growthKey == 'netIncome':
# 					PYval = PYObj.netIncome
# 			except:
# 				PYval = None
# 			i += 1
# 			if PYval and CYval:
# 				growth = calGrowthFormulaView(CYval, PYval, i)
# 				calculatedGrowth[i] = growth
# 	if lengthOfQuerySet >= 4:
# 		CYval = PYval = None
# 		firstElem = querySetForGrowth.first()
# 		lastElem = querySetForGrowth.last()
# 		if growthKey == 'totalRevenue':
# 			CYval = firstElem.totalRevenue
# 		elif growthKey == 'revenue':
# 			CYval = firstElem.revenue
# 		elif growthKey == 'netIncome':
# 			CYval = firstElem.netIncome
# 		CYYear = firstElem.year
# 		try:
# 			PYObj = querySetForGrowth.get(year=CYYear - 1)
# 			if growthKey == 'totalRevenue':
# 				PYval = PYObj.totalRevenue
# 			elif growthKey == 'revenue':
# 				PYval = PYObj.revenue
# 			elif growthKey == 'netIncome':
# 				PYval = PYObj.netIncome
# 		except:
# 			pass
# 		if CYval and PYval:
# 			growth = calGrowthFormulaView(CYval, PYval, 1)
# 			calculatedGrowth[1] = growth
# 		PYval = None
# 		checkBest1 = lengthOfQuerySet//2
# 		midYearObjs = querySetForGrowth[checkBest1-1:checkBest1]
# 		evenNum = False
# 		if (lengthOfQuerySet % 2) == 0:
# 			evenNum = True
# 		for item in midYearObjs:
# 			# if growthKey == 'totalRevenue':
# 			# 	CYval = item.totalRevenue
# 			# elif growthKey == 'revenue':
# 			# 	CYval = item.revenue
# 			# elif growthKey == 'netIncome':
# 			# 	CYval = item.netIncome
# 			midYearObjYear = item.year
# 		if midYearObjYear:
# 			try:
# 				PYObj = querySetForGrowth.get(year = midYearObjYear - 1)
# 				if growthKey == 'totalRevenue':
# 					PYval = PYObj.totalRevenue
# 				elif growthKey == 'revenue':
# 					PYval = PYObj.revenue
# 				elif growthKey == 'netIncome':
# 					PYval = PYObj.netIncome
# 				midYearObjYearForEven = item.year
# 			except:
# 				PYval = None
# 			growth1 = calGrowthFormulaView(CYval, PYval, checkBest1)
# 			growth2 = 0
# 			if evenNum:
# 				# CYval = PYval
# 				try:
# 					PYObj = querySetForGrowth.get(year = midYearObjYear - 2)
# 					if growthKey == 'totalRevenue':
# 						PYval = PYObj.totalRevenue
# 					elif growthKey == 'revenue':
# 						PYval = PYObj.revenue
# 					elif growthKey == 'netIncome':
# 						PYval = PYObj.netIncome
# 					midYearObjYearForEven = item.year
# 				except:
# 					PYval = None
# 				if CYval and PYval:
# 					growth2 = calGrowthFormulaView(CYval, PYval, checkBest1 + 1)
# 			try:
# 				DecimalGrowth1 = Decimal(growth1)
# 			except:
# 				DecimalGrowth1 = None
# 			try:
# 				DecimalGrowth2 = Decimal(growth2)
# 			except:
# 				DecimalGrowth2 = None
# 			if DecimalGrowth1 and DecimalGrowth2:
# 				if DecimalGrowth1 > DecimalGrowth2:
# 					calculatedGrowth[checkBest1] = growth1
# 				else:
# 					calculatedGrowth[checkBest1 - 1] = growth2
# 			elif DecimalGrowth1 and not DecimalGrowth2:
# 				calculatedGrowth[checkBest1] = growth1
# 			elif not DecimalGrowth2 == None:
# 				calculatedGrowth[checkBest1 - 1] = growth2
# 		PYval = None
# 		try:
# 			CYYear = lastElem.year + 1
# 			# CYObj = querySetForGrowth.get(year = CYYear)
# 			if growthKey == 'totalRevenue':
# 				# CYval = CYObj.totalRevenue
# 				PYval = lastElem.totalRevenue
# 			elif growthKey == 'revenue':
# 				# CYval = CYObj.revenue
# 				PYval = lastElem.revenue
# 			elif growthKey == 'netIncome':
# 				# CYval = CYObj.netIncome
# 				PYval = lastElem.netIncome
# 		except:
# 			pass
# 		if CYval and PYval:
# 			growth = calGrowthFormulaView(CYval, PYval, lengthOfQuerySet)
# 			calculatedGrowth[lengthOfQuerySet] = growth
# 	return (calculatedGrowth)

#
# def calculateForListGrowthNew(objList, growthKey):
# 	listLength = 0
# 	if objList:
# 		listLength = len(objList) - 1
# 	calculatedGrowth = {}
# 	if listLength >= 1 and listLength < 4:
# 		i = 0
# 		for item in objList:
# 			CYYear = item.year
# 			if i == 0:
# 				if growthKey == 'roe':
# 					CYval = item.value
# 			try:
# 				PYObj = objList[i+1]
# 				if growthKey == 'roe':
# 					PYval = PYObj.value
# 			except:
# 				PYval = None
# 			i += 1
# 			if PYval and CYval:
# 				growth = calGrowthFormulaView(CYval, PYval, i)
# 				calculatedGrowth[i] = growth
# 	if listLength >= 4:
# 		CYval = PYval = None
# 		firstElem = objList[0]
# 		lastElem = objList[-1]
# 		if growthKey == 'roe':
# 			CYval = firstElem.value
# 		CYYear = firstElem.year
# 		try:
# 			PYObj = objList[1]
# 			if growthKey == 'roe':
# 				PYval = PYObj.value
# 		except:
# 			pass
# 		if CYval and PYval:
# 			growth = calGrowthFormulaView(CYval, PYval, 1)
# 			calculatedGrowth[1] = growth

# 		PYval = None
# 		checkBest1 = listLength//2
# 		midYearObjs = objList[checkBest1:checkBest1+1]
# 		evenNum = False
# 		if (listLength % 2) == 0:
# 			evenNum = True
# 		for item in midYearObjs:
# 			CYYearMid = item.year
# 			# if growthKey == 'roe':
# 			# 	CYval = item.value
# 		try:
# 			PYObj = objList[checkBest1 + 1]
# 			if growthKey == 'roe':
# 				PYval = PYObj.value
# 			PYYearMID = PYObj.year
# 		except:
# 			PYval = None
# 		if evenNum:
# 			newNForCY = checkBest1
# 		else:
# 			newNForCY = checkBest1 + 1
# 		growth1 = calGrowthFormulaView(CYval, PYval, newNForCY)
# 		growth2 = 0
# 		if evenNum:
# 			# CYval = PYval
# 			try:
# 				PYObj = objList[checkBest1 + 2]
# 				if growthKey == 'roe':
# 					PYval = PYObj.value
# 			except:
# 				PYval = None
# 			if CYval and PYval:
# 				growth2 = calGrowthFormulaView(CYval, PYval, checkBest1 + 1)
# 		try:
# 			DecimalGrowth1 = Decimal(growth1)
# 		except:
# 			DecimalGrowth1 = None
# 		try:
# 			DecimalGrowth2 = Decimal(growth2)
# 		except:
# 			DecimalGrowth2 = None
# 		if DecimalGrowth1 and DecimalGrowth2:
# 			if DecimalGrowth1 > DecimalGrowth2:
# 				calculatedGrowth[checkBest1] = growth1
# 			else:
# 				calculatedGrowth[checkBest1 - 1] = growth2
# 		elif DecimalGrowth1 and not DecimalGrowth2:
# 			calculatedGrowth[checkBest1] = growth1
# 		elif not DecimalGrowth2 == None:
# 			calculatedGrowth[checkBest1 - 1] = growth2

# 		PYval = None
# 		try:
# 			CYYear = lastElem.year + 1
# 			CYObj = objList[-2]
# 			if growthKey == 'roe':
# 				# CYval = CYObj.value
# 				PYval = lastElem.value
# 		except:
# 			pass
# 		if CYval and PYval:
# 			growth = calGrowthFormulaView(CYval, PYval, listLength)
# 			calculatedGrowth[listLength] = growth
# 	return (calculatedGrowth)

def welcomeLoginPopupView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(welcomeLoginPopup, pk=pkID)
        objForm = welcomeLoginPopupForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, f'Please check following errors: {objForm.errors}')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockListView(request):
    allStocks = stockBasicDetail.objects.all().order_by('stockName')
    createStockBasicDetail = stockBasicDetailForm()
    currentBondRateCreate = currentRateOfbondYieldForm()

    try:
        lastestBondRate = currentRateOfbondYield.objects.latest('id')
    except:
        lastestBondRate = None
    try:
        lastestSchema = stockAppSpecific.objects.latest('id')
    except:
        lastestSchema = None
    try:
        latestDMForStockList = stockListDM.objects.latest('id')
    except:
        latestDMForStockList = None
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
    except:
        iDescriptionForKeyRatiosInst = None
    createiDescriptionForKeyRatiosForm = iDescriptionForKeyRatiosForm(instance=iDescriptionForKeyRatiosInst)

    try:
        stockListHeadingInst = stockListHeading.objects.latest('id')
    except:
        stockListHeadingInst = None
    createstockListHeadingForm = stockListHeadingForm()

    yearlyRBIData = valuesRBIStandards.objects.all().order_by('year')
    valuesRBIStandardsCreate = valuesRBIStandardsForm()

    # welcomeLoginPopupInstForm = welcomeLoginPopupForm(instance=popupInst)

    # print(f'this is welcome login instance {popupInst.letsBeginContent}')

    context = {
        # 'popupInst':popupInst,
        # 'welcomeLoginPopupInstForm':welcomeLoginPopupInstForm,
        'stocks': allStocks,
        'stockListHeadingInst': stockListHeadingInst,
        'createstockListHeadingForm': createstockListHeadingForm,
        'createStockBasicDetail': createStockBasicDetail,
        'currentBondRateCreate': currentBondRateCreate,
        'lastestBondRate': lastestBondRate,
        'lastestSchema': lastestSchema,
        'latestDMForStockList': latestDMForStockList,
        'createiDescriptionForKeyRatiosForm': createiDescriptionForKeyRatiosForm,
        'valuesRBIStandardsCreate': valuesRBIStandardsCreate,
        'yearlyRBIData': yearlyRBIData,
    }
    return render(request, 'UI/stockList.html', context)


#
def processDictForGrowthFormula(getDict, yearIs='key', requestFrom=None):
    totalYearsData = []
    processedDict = {}
    if yearIs == 'key':
        for key, val in getDict.items():
            totalYearsData.append(key)
    if (len(totalYearsData) > 1):
        CYear = totalYearsData[0]
        if requestFrom == 'keyRatioIndusSpecific':
            CYval = getDict.get(CYear)
        for i, j in enumerate(totalYearsData[:-1]):
            forloopCounter = i + 1
            firstYear = j
            prevYear = totalYearsData[i + 1]
            n = CYear - prevYear
            if requestFrom == 'keyRatioIndusSpecific':
                PYval = getDict.get(prevYear)
            processedDict[forloopCounter] = round(calGrowthFormulaViewForIndusSpecific(CYval, PYval, n), 2)
    return processedDict


#
def calGrowthFormulaViewForIndusSpecific(CYval=0.00, PYval=0.00, years=1.00):
    if CYval == None or PYval == None:
        return False
    else:
        if PYval == 0:
            PYval = 1
        dividedVal = CYval / PYval
        powerVal = 1 / years
        poweredVal = pow(float(dividedVal), float(powerVal))
        calVal = (poweredVal - 1) * 100
        return calVal


#
# def intrinsicFormula(stock):
# 	calVal = None
# 	try:
# 		lastestBondRateObj = currentRateOfbondYield.objects.latest('id')
# 		lastestBondRate = lastestBondRateObj.value
# 	except:
# 		lastestBondRate = None
# 	if lastestBondRate:
# 		try:
# 			stockEssObj = stockEssentials.objects.get(stockProfileName=stock)
# 			salesGrowthRateOfXYearVal = stockEssObj.salesGrowthRateOfXYear
# 		except:
# 			salesGrowthRateOfXYearVal = None
# 		try:
# 			stockProfLossObj = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
# 			dilutedEps = stockProfLossObj.dilutedEPS
# 			basicEps = stockProfLossObj.basicEPS
# 		except:
# 			basicEps = dilutedEps = None
# 		eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
# 		if salesGrowthRateOfXYearVal:
# 			if eps:
# 				calVal = eps * (Decimal(8.5) + (Decimal(2) * salesGrowthRateOfXYearVal)) * (Decimal(8.5) / lastestBondRate)
# 				calVal = round(calVal,2)
# 	return calVal

#
def intrinsicFormula(stock, forNBFC=False):
    calVal = currentYear = totalRevenue = None
    try:
        if forNBFC:
            stockProfLossObj = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            totalRevenue = stockProfLossObj.totalRevenue
        else:
            stockProfLossObj = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
            totalRevenue = stockProfLossObj.revenue
        currentYear = stockProfLossObj.year
        dilutedEps = stockProfLossObj.dilutedEPS
        basicEps = stockProfLossObj.basicEPS
    except:
        basicEps = dilutedEps = None
    if currentYear:
        fifthYear = currentYear - 5
        try:
            if forNBFC:
                fifththProfLoss = stockProfitAndLossBankNBFC.objects.get(stockProfileName=stock, year=fifthYear)
                totalRevenueFifthYear = fifththProfLoss.totalRevenue
            else:
                fifththProfLoss = stockProfitAndLoss.objects.get(stockProfileName=stock, year=fifthYear)
                totalRevenueFifthYear = fifththProfLoss.revenue
        except:
            totalRevenueFifthYear = None
    try:
        lastestBondRateObj = currentRateOfbondYield.objects.latest('id')
        latestBondRate = lastestBondRateObj.value
    except:
        latestBondRate = 1
    # currentPrice = localOrScreenerPriceView(stock)
    eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
    if totalRevenue and totalRevenueFifthYear and eps:
        growthRate = totalRevenue / totalRevenueFifthYear
        growthRate = pow(growthRate, convert_to_decimal(0.2))
        growthRate = growthRate - 1
        growthRate = round(growthRate, 6)
        val1 = convert_to_decimal(2) * convert_to_decimal(growthRate) * convert_to_decimal(100)
        val2 = convert_to_decimal(8.5) + convert_to_decimal(val1)
        val3 = val2 * convert_to_decimal(eps)
        val4 = convert_to_decimal(8.5) / latestBondRate
        calVal = val3 * val4
        return calVal
    else:
        return calVal


#
def calGrowthTemplateDataView(stock, requestFrom=None):
    returnRevenueGrowthData = {}
    returnRevenueGrowthAlgoProgrammedData = {}
    returnNetProfitGrowthData = {}
    returnNetProfitAlgoProgrammedData = {}
    returnEPSGrowthData = {}
    returnEPSAlgoProgrammedData = {}
    returnEBITDAGrowthData = {}
    returnEBITDAAlgoProgrammedData = {}
    returnPBITGrowthData = {}
    returnPBITAlgoProgrammedData = {}
    totalYearsData = []
    totalData = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('-year')
    for item in totalData:
        totalYearsData.append(item.year)
    if (len(totalYearsData) > 1):
        CYear = totalYearsData[0]
        CY = stockProfitAndLoss.objects.get(stockProfileName=stock, year=CYear)
        for i, j in enumerate(totalYearsData[:-1]):
            forloopCounter = i + 1
            firstYear = j
            prevYear = totalYearsData[i + 1]
            n = CYear - prevYear
            PY = stockProfitAndLoss.objects.get(stockProfileName=stock, year=prevYear)
            # revenue
            calculatedRevGrowth = (calGrowthFormulaView(CY.totalRevenue, PY.totalRevenue, n))
            if calculatedRevGrowth:
                returnRevenueGrowthData[n] = calculatedRevGrowth
                # revenueForGrowth
                returnRevenueGrowthAlgoProgrammedData[forloopCounter] = calculatedRevGrowth
            # PAT
            CYEBITDA = return_val_or_0(CY.ebidta)
            CYPBIT = return_val_or_0(CY.pbit)
            CYPBT = return_val_or_0(CY.pbt)
            CYPAT = return_val_or_0(CY.netIncome)
            PYEBITDA = return_val_or_0(PY.ebidta)
            PYPBIT = return_val_or_0(PY.pbit)
            PYPBT = return_val_or_0(PY.pbt)
            PYPAT = return_val_or_0(PY.netIncome)
            calculatedPATGrowth = (calGrowthFormulaView(CYPAT, PYPAT, n))
            if calculatedPATGrowth:
                returnNetProfitGrowthData[n] = calculatedPATGrowth
                # PATForGrowth
                returnNetProfitAlgoProgrammedData[forloopCounter] = calculatedPATGrowth
            # EPS
            CYEps = return_val_or_0(CY.basicEPS)
            PYEps = return_val_or_0(PY.basicEPS)
            calculatedEPSGrowth = (calGrowthFormulaView(CYEps, PYEps, n))
            if calculatedEPSGrowth:
                returnEPSGrowthData[n] = calculatedEPSGrowth
                # EPSForGrowth
                returnEPSAlgoProgrammedData[forloopCounter] = calculatedEPSGrowth
            # EBITDA
            calculatedEBITDAGrowth = (calGrowthFormulaView(CYEBITDA, PYEBITDA, n))
            if calculatedEBITDAGrowth:
                returnEBITDAGrowthData[n] = calculatedEBITDAGrowth
                # EBITDAForGrowth
                returnEBITDAAlgoProgrammedData[forloopCounter] = calculatedEBITDAGrowth
            # PBIT

            calculatedPBITGrowth = (calGrowthFormulaView(CYPBIT, PYPBIT, n))
            if calculatedPBITGrowth:
                returnPBITGrowthData[n] = calculatedPBITGrowth
                # PBITForGrowth
                returnPBITAlgoProgrammedData[forloopCounter] = calculatedPBITGrowth
    if requestFrom == 'snapshot':
        return returnRevenueGrowthData, returnNetProfitAlgoProgrammedData
    else:
        return returnRevenueGrowthData, returnRevenueGrowthAlgoProgrammedData, returnNetProfitGrowthData, returnNetProfitAlgoProgrammedData, returnEPSGrowthData, returnEPSAlgoProgrammedData, returnEBITDAGrowthData, returnEBITDAAlgoProgrammedData, returnPBITGrowthData, returnPBITAlgoProgrammedData


def marketCapView(stock):
    try:
        essentialInst = stockEssentials.objects.get(stockProfileName=stock)
    except:
        essentialInst = None
    if essentialInst:
        totalSharesInst = essentialInst.totalShares
    else:
        totalSharesInst = 0
    # try:
    # 	currentStockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
    # 	currentStockPrice = currentStockPriceInst.investorPrice
    # except:
    # 	currentStockPrice = 0
    currentStockPrice = localOrScreenerPriceView(stock)

    try:
        marketCap = (totalSharesInst * currentStockPrice) / 10000000
    except:
        marketCap = None

    return marketCap


#
def returnDecimalOrZero(passedNo):
    if passedNo == None:
        passedNo = Decimal(0)
    else:
        passedNo = Decimal(passedNo)
    return passedNo


#
def localOrScreenerPriceView(stock):
    stockPrice = None
    try:
        essentialInst = stockEssentials.objects.get(stockProfileName=stock)
    except:
        essentialInst = None
    screenerPriceCats = categoryOptions.objects.filter(fetchScreenerPrice=True)
    if essentialInst and essentialInst.category in screenerPriceCats:
        stockPrice = getScreenerPriceForStock(essentialInst)
    else:
        try:
            stockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
            stockPrice = stockPriceInst.investorPrice
        except:
            pass
    return stockPrice


#
def snapshotView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    print(f'Non NBFC snap Hit: {stock}')
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl', permanent=True)

    renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
    if renderBankNBFCsTemplates:
        return snapshotForBankNBFCsView(request, slug)

    currentPrice = localOrScreenerPriceView(stock)
    callingFunction = 'snapshot'
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None
    createStockAdmin = stockAdminForm(instance=stockAdmInst)
    createStockAdminSnapshot = stockAdminSnapshotForm(instance=stockAdmInst)

    try:
        benGrahamOrDCFInst = benGrahamOrDCF.objects.get(stockProfileName=stock)
    except:
        benGrahamOrDCFInst = None
    benGrahamOrDCFCreate = benGrahamOrDCFForm(instance=benGrahamOrDCFInst)

    try:
        essentialInst = stockEssentials.objects.get(stockProfileName=stock)
    except:
        essentialInst = None
    createStockEssentials = stockEssentialsForm(instance=essentialInst)
    createStockEssentialsBottom = stockEssentialsBottomForm(instance=essentialInst)

    try:
        stockInvestmentChecklistInst = stockInvestmentChecklist.objects.get(stockProfileName=stock)
    except:
        stockInvestmentChecklistInst = None
    createstockInvestmentChecklist = stockInvestmentChecklistForm(instance=stockInvestmentChecklistInst)

    try:
        stockIPOInst = stockIPO.objects.get(stockProfileName=stock)
    except:
        stockIPOInst = None
    createStockIPO = stockIPOForm(instance=stockIPOInst)

    try:
        stockDetailsInst = stockDetails.objects.get(stockProfileName=stock)
    except:
        stockDetailsInst = None
    createStockDetails = stockDetailsFormMergerAcquistion(instance=stockDetailsInst)
    createSubsidiariesBusModelStockDetails = stockDetailsSubsidiariesBusModelForm(instance=stockDetailsInst)
    createProductStockDetails = stockDetailsProductForm(instance=stockDetailsInst)
    createAssestStockDetails = stockDetailsAssestForm(instance=stockDetailsInst)
    createIndustryOverviewStockDetails = stockDetailsIndustryOverviewForm(instance=stockDetailsInst)
    createStockAbout = stockDetailsAboutForm(instance=stockDetailsInst)
    createawardsDescription = stockDetailsAwardForm(instance=stockDetailsInst)
    createSSOTDescription = stockDetailsSSOTForm(instance=stockDetailsInst)

    revenueBreakupInst = stockRevenueBreakUp.objects.filter(stockProfileName=stock)
    viewStockRevenueBreakUpForm = stockRevenueBreakUpForm()

    try:
        stockFundingInst = stockFunding.objects.get(stockProfileName=stock)
    except:
        stockFundingInst = None
    createStockFunding = stockFundingForm(instance=stockFundingInst)

    stockFundingRoundsInst = stockFundingRounds.objects.filter(stockProfileName=stock).order_by('-dateOfInvestment')
    createStockFundingRounds = stockFundingRoundsForm()

    try:
        promotorHolding = stockOwnershipPattern.objects.get(stockProfileName=stock, year=currentYear)
        promotorHolding = promotorHolding.totalPromoterholdingValue
    except:
        promotorHolding = None
    try:
        latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
        totalRevCY = latestProfitAndLoss.totalRevenue
        patCY = latestProfitAndLoss.netIncome
        epsCY = latestProfitAndLoss.basicEPS
        dps = latestProfitAndLoss.DPS
    except:
        totalRevCY = None
        patCY = None
        epsCY = None
        dps = None
    try:
        latestCashFlow = stockCashFlow.objects.filter(stockProfileName=stock).latest('year')
        cashFlowOperationsCY = latestCashFlow.cashFromOperatingActivities
        cashFlowFinancingCY = latestCashFlow.cashFromFinancingActivities
    except:
        cashFlowOperationsCY = None
        cashFlowFinancingCY = None

    categoryForEss = categoryOptions.objects.all().order_by('name')
    sectorForEss = sectorOptions.objects.all().order_by('name')
    subSectorForEss = subSectorOptions.objects.all().order_by('name')
    returnedGrowthROEVal = ROEgrowthCalculator(stock)
    # return returnedGrowthROEVal
    intrinsicVal = intrinsicFormula(stock)
    returnedRevenueGrowthAlgoProgrammedData, processedNetProfitGrowthTextual = calGrowthTemplateDataView(stock,
                                                                                                         requestFrom='snapshot')
    compoundSalesGrowth = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    # compoundProfitGrowth = calculateProgrammedGrowth(processedNetProfitGrowthTextual)
    despositoryOptions, saleType = rightSideMenuObjs()
    profitAndLossQuerySet = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('-year')
    revenueGrowth = calculateGrowthNew(profitAndLossQuerySet, 'revenue')
    compoundProfitGrowth = calculateGrowthNew(profitAndLossQuerySet, 'netIncome')
    try:
        bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
        bookValYear = bookValues.year
        totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=bookValYear)
        bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
    except:
        bookValues = bookValueCal = None

    try:
        fundingRoundsUnitInst = get_object_or_404(foundingRoundsFigureUnits, stockProfileName=stock)
    except:
        fundingRoundsUnitInst = None
    fundingRoundsUnitCreate = foundingRoundsFigureUnitsForm()

    try:
        fundingDetailsVisibilityInst = get_object_or_404(fundingDetailsVisibility, stockProfileName=stock)
    except:
        fundingDetailsVisibilityInst = None
    fundingDetailsVisibilityCreate = fundingDetailsVisibilityForm()

    if essentialInst:
        totalSharesInst = essentialInst.totalShares
    else:
        totalSharesInst = 0

    try:
        stockProfitAndLossInst = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
        basicEps = stockProfitAndLossInst.basicEPS
        dilutedEps = stockProfitAndLossInst.dilutedEPS
    except:
        basicEps = 1
        dilutedEps = 1

    eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
    try:
        PEvalue = round((currentPrice / eps), 2)
    except:
        PEvalue = None

    if bookValues:
        bookVal = bookValueCal
    else:
        bookVal = 1
    try:
        PBvalue = round((currentPrice / bookVal), 2)
    except:
        PBvalue = None

    try:
        earningsYield = round((epsCY / currentPrice) * 100, 2)
    except:
        earningsYield = None

    try:
        dividendYield = round((dps / currentPrice) * 100, 2)
    except:
        dividendYield = None

    # enterprise value
    cashAndShortTermEqui = minorityInt = 0
    try:
        stockBalanceSheetLatestObj = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
        cashAndShortTermEqui = stockBalanceSheetLatestObj.cashAndShortTermInvestments
        minorityInt = stockBalanceSheetLatestObj.minorityInterest
    except:
        pass
    balWithRBI = prefEquity = 0
    try:
        balWithRBI = essentialInst.balance_with_RBI
        prefEquity = essentialInst.preference_equity
    except:
        pass

    if not balWithRBI:
        balWithRBI = 0
    if not prefEquity:
        prefEquity = 0
    totalLngDebt = currPortLngTermDebt = currPortionLeases = lngTermPortionOfLeases = 0
    try:
        latestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
        if latestBalanceSheet.totalLongTermDebt:
            totalLngDebt = Decimal(latestBalanceSheet.totalLongTermDebt)
        if latestBalanceSheet.currentPortionOfLongTermDebt:
            currPortLngTermDebt = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
        if latestBalanceSheet.currentPortionOfLeases:
            currPortionLeases = Decimal(latestBalanceSheet.currentPortionOfLeases)
        if latestBalanceSheet.longTermPortionOfLeases:
            lngTermPortionOfLeases = Decimal(latestBalanceSheet.longTermPortionOfLeases)
    except:
        pass
    totalDebt = totalLngDebt + currPortionLeases + lngTermPortionOfLeases + currPortLngTermDebt
    try:
        marketCap = (totalSharesInst * currentPrice) / 10000000
        marketCapForEnterprise = marketCap
    except:
        marketCap = None
        marketCapForEnterprise = None
    try:
        marketCapForEnterprise = numberConversion(marketCapForEnterprise, currentSystem='Cr',
                                                  convertTo=stock.stockProfileNameFFU.financialNumbers)
    except:
        pass

    enterpriseVal = returnDecimalOrZero(marketCapForEnterprise) - (
            returnDecimalOrZero(cashAndShortTermEqui) - returnDecimalOrZero(balWithRBI)) + returnDecimalOrZero(
        totalDebt) + returnDecimalOrZero(prefEquity) + returnDecimalOrZero(minorityInt)
    try:
        enterpriseVal = numberConversion(enterpriseVal, currentSystem=stock.stockProfileNameFFU.financialNumbers,
                                         convertTo='Cr')
    except:
        pass

    researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
    researchReportFAQsInstForm = researchReportFAQsForm()

    totalShareYearlyDataInst = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                   shareType='financial_year').order_by('year')
    totalShareYearlyDataInstConvertible = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                              shareType='convertible_equity').order_by(
        'year')
    totalShareYearlyDataInstForm = totalShareYearlyDataForm()

    commonFAQInst = commonFAQ.objects.all().order_by('id')
    commonFAQInstForm = commonFAQForm()
    try:
        newsVideosheadfinancial = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    # print(newsVideosheadfinancial)
    except:
        newsVideosheadfinancial = []

    context = {
        'newsVideosheadfinancial': newsVideosheadfinancial,
        'bookValues': bookValues,
        'revenueGrowth': revenueGrowth,
        'essentialInst': essentialInst,
        'createStockEssentials': createStockEssentials,
        'createStockEssentialsBottom': createStockEssentialsBottom,
        'stockInvestmentChecklistInst': stockInvestmentChecklistInst,
        'createstockInvestmentChecklist': createstockInvestmentChecklist,
        'stockIPOInst': stockIPOInst,
        'createStockIPO': createStockIPO,
        'stockDetailsInst': stockDetailsInst,
        'createStockDetails': createStockDetails,
        'createSubsidiariesBusModelStockDetails': createSubsidiariesBusModelStockDetails,
        'createProductStockDetails': createProductStockDetails,
        'createAssestStockDetails': createAssestStockDetails,
        'createIndustryOverviewStockDetails': createIndustryOverviewStockDetails,
        'stockFundingInst': stockFundingInst,
        'createStockFunding': createStockFunding,
        'stockFundingRoundsInst': stockFundingRoundsInst,
        'createStockFundingRounds': createStockFundingRounds,
        'promotorHolding': promotorHolding,
        'stockAdmInst': stockAdmInst,
        'createStockAdmin': createStockAdmin,
        'createStockAdminSnapshot': createStockAdminSnapshot,
        'createStockAbout': createStockAbout,
        'createawardsDescription': createawardsDescription,
        'createSSOTDescription': createSSOTDescription,
        'compoundSalesGrowth': compoundSalesGrowth,
        'compoundProfitGrowth': compoundProfitGrowth,
        'totalRevCY': totalRevCY,
        'patCY': patCY,
        'epsCY': epsCY,
        'cashFlowOperationsCY': cashFlowOperationsCY,
        'cashFlowFinancingCY': cashFlowFinancingCY,
        'categoryForEss': categoryForEss,
        'sectorForEss': sectorForEss,
        'subSectorForEss': subSectorForEss,
        'returnedGrowthROEVal': returnedGrowthROEVal,
        'intrinsicVal': intrinsicVal,
        'revenueBreakupInst': revenueBreakupInst,
        'viewStockRevenueBreakUpForm': viewStockRevenueBreakUpForm,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'stock': stock,
        'fundingRoundsUnitInst': fundingRoundsUnitInst,
        'fundingRoundsUnitCreate': fundingRoundsUnitCreate,
        'fundingDetailsVisibilityInst': fundingDetailsVisibilityInst,
        'fundingDetailsVisibilityCreate': fundingDetailsVisibilityCreate,
        'benGrahamOrDCFInst': benGrahamOrDCFInst,
        'benGrahamOrDCFForm': benGrahamOrDCFCreate,
        'marketCap': marketCap,
        'PEvalue': PEvalue,
        'PBvalue': PBvalue,
        'earningsYield': earningsYield,
        'dividendYield': dividendYield,
        'bookValueCal': bookValueCal,
        'enterpriseVal': enterpriseVal,
        'researchReportFAQsInst': researchReportFAQsInst,
        'researchReportFAQsInstForm': researchReportFAQsInstForm,
        'totalShareYearlyDataInst': totalShareYearlyDataInst,
        'totalShareYearlyDataInstConvertible': totalShareYearlyDataInstConvertible,
        'totalShareYearlyDataInstForm': totalShareYearlyDataInstForm,
        'commonFAQInst': commonFAQInst,
        'commonFAQInstForm': commonFAQInstForm,
    }
    return render(request, 'UI/snapshotNewDesign.html', context)

#
def faqs_view(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    commonFAQInst = commonFAQ.objects.all().order_by('id')
    commonFAQInstForm = commonFAQForm()
    researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
    researchReportFAQsInstForm = researchReportFAQsForm()
    context = {
        'commonFAQInst': commonFAQInst,
        'commonFAQInstForm': commonFAQInstForm,
        'researchReportFAQsInst': researchReportFAQsInst,
        'researchReportFAQsInstForm': researchReportFAQsInstForm,
        'stock': stock,
    }
    return render(request, 'UI/faqs.html', context)

#
def ownershipView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)

    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    try:
        ownershipInst = stockOwnership.objects.get(stockProfileName=stock)
    except:
        ownershipInst = None
    createStockOwnership = stockOwnershipForm(instance=ownershipInst)

    ownershipDirectorInst = stockOwnershipDirector.objects.filter(stockProfileName=stock)
    createStockOwnershipDirector = stockOwnershipDirectorForm()

    ownershipInstitutionalInst = stockOwnershipInstitutional.objects.filter(stockProfileName=stock)
    createStockOwnershipInstitutional = stockOwnershipInstitutionalForm()

    ownershipPatternInst = stockOwnershipPattern.objects.filter(stockProfileName=stock).order_by('-year')
    totalPromoterholdingValue = mutualFundHoldingValue = domesticInstitutionalHoldingsValue = foreignInstitutionalHoldingsValue = others = institutionalHolding = publicInstitutionalHoldings = nonPublicInstitutionalHoldings = retail = employees = custodians = promoters = privatePublicInvestmenFirmVCs = False

    for item in ownershipPatternInst:
        if item.totalPromoterholdingValue:
            totalPromoterholdingValue = True
        if item.mutualFundHoldingValue:
            mutualFundHoldingValue = True
        if item.domesticInstitutionalHoldingsValue:
            domesticInstitutionalHoldingsValue = True
        if item.foreignInstitutionalHoldingsValue:
            foreignInstitutionalHoldingsValue = True
        if item.others:
            others = True
        if item.institutionalHolding:
            institutionalHolding = True
        if item.publicInstitutionalHoldings:
            publicInstitutionalHoldings = True
        if item.nonPublicInstitutionalHoldings:
            nonPublicInstitutionalHoldings = True
        if item.retail:
            retail = True
        if item.employees:
            employees = True
        if item.custodians:
            custodians = True
        if item.promoters:
            promoters = True
        if item.privatePublicInvestmenFirmVCs:
            privatePublicInvestmenFirmVCs = True

    createStockPatternInstitutional = stockOwnershipPatternForm()

    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None
    despositoryOptions, saleType = rightSideMenuObjs()
    staticUrl = settings.STATIC_URL

    try:
        newsVideosheadownership = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadownership = []

    try:
        typeofcompanyInstownership = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstownership = None

    context = {
        'stock': stock,
        'ownershipInst': ownershipInst,
        'newsVideosheadownership': newsVideosheadownership,
        'typeofcompanyInstownership': typeofcompanyInstownership,
        'createStockOwnership': createStockOwnership,
        'ownershipDirectorInst': ownershipDirectorInst,
        'createStockOwnershipDirector': createStockOwnershipDirector,
        'ownershipInstitutionalInst': ownershipInstitutionalInst,
        'createStockOwnershipInstitutional': createStockOwnershipInstitutional,
        'ownershipPatternInst': ownershipPatternInst,
        'createStockPatternInstitutional': createStockPatternInstitutional,
        'stockAdmInst': stockAdmInst,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'staticUrl': staticUrl,
        'totalPromoterholdingValue': totalPromoterholdingValue,
        'mutualFundHoldingValue': mutualFundHoldingValue,
        'domesticInstitutionalHoldingsValue': domesticInstitutionalHoldingsValue,
        'foreignInstitutionalHoldingsValue': foreignInstitutionalHoldingsValue,
        'others': others,
        'institutionalHolding': institutionalHolding,
        'publicInstitutionalHoldings': publicInstitutionalHoldings,
        'nonPublicInstitutionalHoldings': nonPublicInstitutionalHoldings,
        'retail': retail,
        'employees': employees,
        'custodians': custodians,
        'promoters': promoters,
        'privatePublicInvestmenFirmVCs': privatePublicInvestmenFirmVCs,
    }
    return render(request, 'UI/ownership.html', context)


#
def financialView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
    if renderBankNBFCsTemplates:
        return financialForBankNBFCsView(request, slug)
    includeFile = 'UI/financialProfitAndLoss.html'
    activeNavTab = request.GET.get('nav')
    if activeNavTab:
        if activeNavTab == 'profit-and-loss':
            includeFile = 'UI/financialProfitAndLoss.html'
        elif activeNavTab == 'cash-flow':
            includeFile = 'UI/financialCashFlow.html'
        elif activeNavTab == 'balance-sheet':
            includeFile = 'UI/financialBalanceSheet.html'
    fallBackFile = 'UI/financialProfitAndLoss.html'
    tempToInclude = select_template([includeFile, fallBackFile])
    despositoryOptions, saleType = rightSideMenuObjs()

    financialStatementsFrProfitAndLossInst = financialStatementsFrProfitAndLoss.objects.filter(stockProfileName=stock)
    createFinancialStatementsFrProfitAndLoss = financialStatementsFrProfitAndLossForm()

    financialStatementsFrBalanceSheetInst = financialStatementsFrBalanceSheet.objects.filter(stockProfileName=stock)
    createFinancialStatementsFrBalanceSheet = financialStatementsFrBalanceSheetForm()

    financialStatementsFrCashFlowInst = financialStatementsFrCashFlow.objects.filter(stockProfileName=stock)
    createFinancialStatementsFrCashFlow = financialStatementsFrCashFlowForm()

    financialCompanyUpdatesInst = financialCompanyUpdates.objects.filter(stockProfileName=stock).order_by('title')
    createFinancialCompanyUpdates = financialCompanyUpdatesForm()

    stockProfitAndLossInst = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')
    createstockProfitAndLoss = stockProfitAndLossForm()

    stockBalanceSheetInst = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('year')
    createStockBalanceSheet = stockBalanceSheetForm()

    stockCashFlowInst = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')
    createStockCashFlow = stockCashFlowForm()

    stockDeckAndDocsInst = stockDeckAndDocs.objects.filter(stockProfileName=stock).order_by('-id')
    stockDeckAndDocsInstForm = stockDeckAndDocsForm()

    try:
        figureUnitInst = get_object_or_404(financialFigureUnits, stockProfileName=stock)
    except:
        figureUnitInst = None
    financialFigureUnitsCreate = financialFigureUnitsForm()

    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None

    try:
        annualReportsDHRPInst = annualReportsDHRP.objects.get(stockProfileName=stock)
    except:
        annualReportsDHRPInst = None
    createAnnualReportsDHRP = annualReportsDHRPForm(instance=annualReportsDHRPInst)

    try:
        annualReportsDHRPImageInst = annualReportsDHRPImage.objects.filter(stockProfileName=stock)
        annualReportsDHRPImage_serializer = annualReportsDHRPImageSerializer(annualReportsDHRPImageInst, many=True)
        annualReportsDHRPImage_data = annualReportsDHRPImage_serializer.data
        annualReportsDHRPImage_data = json.dumps(annualReportsDHRPImage_data)
        annualReportsDHRPImage_serialized_data = json.loads(annualReportsDHRPImage_data)
    except:
        annualReportsDHRPImageInst = None

    try:
        annualReportsDHRPImageInstcreate = annualReportsDHRPImage.objects.get(stockProfileName=stock)
    except:
        annualReportsDHRPImageInstcreate = None
    createannualReportsDHRPImage = annualReportsDHRPImageForm(instance=annualReportsDHRPImageInstcreate)

    try:
        balanceSheetTTMInst = stockBalanceSheetTTM.objects.get(stockProfileName=stock)
    except:
        balanceSheetTTMInst = None
    createStockBalanceSheetTTM = stockBalanceSheetTTMForm(instance=balanceSheetTTMInst)

    try:
        profitAndLossTTMInst = stockProfitAndLossTTM.objects.get(stockProfileName=stock)
    except:
        profitAndLossTTMInst = None
    createStockProfitAndLossTTM = stockProfitAndLossTTMForm(instance=profitAndLossTTMInst)

    try:
        cashFlowTTMInst = stockCashFlowTTM.objects.get(stockProfileName=stock)
    except:
        cashFlowTTMInst = None
    createCashFlowTTM = stockCashFlowTTMForm(instance=cashFlowTTMInst)

    # description field for SEO - starts
    try:
        stockFinBalanceSheetSEOInst = stockFinBalanceSheetSEO.objects.get(stockProfileName=stock)
    except:
        stockFinBalanceSheetSEOInst = None
    createStockFinBalanceSheetSEO = stockFinBalanceSheetSEOForm(instance=stockFinBalanceSheetSEOInst)
    # description field for SEO - ends
    try:
        newsVideosheadfinancial = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadfinancial = []

    try:
        typeofcompanyInst = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInst = None

    context = {
        'stock': stock,
        'includeFile': includeFile,
        'newsVideosheadfinancial': newsVideosheadfinancial,
        'typeofcompanyInst': typeofcompanyInst,
        'financialStatementsFrProfitAndLossInst': financialStatementsFrProfitAndLossInst,
        'createFinancialStatementsFrProfitAndLoss': createFinancialStatementsFrProfitAndLoss,
        'financialStatementsFrBalanceSheetInst': financialStatementsFrBalanceSheetInst,
        'createFinancialStatementsFrBalanceSheet': createFinancialStatementsFrBalanceSheet,
        'financialStatementsFrCashFlowInst': financialStatementsFrCashFlowInst,
        'createFinancialStatementsFrCashFlow': createFinancialStatementsFrCashFlow,
        'financialCompanyUpdatesInst': financialCompanyUpdatesInst,
        'createFinancialCompanyUpdates': createFinancialCompanyUpdates,
        'stockProfitAndLossInst': stockProfitAndLossInst,
        'createstockProfitAndLoss': createstockProfitAndLoss,
        'stockBalanceSheetInst': stockBalanceSheetInst,
        'createStockBalanceSheet': createStockBalanceSheet,
        'stockCashFlowInst': stockCashFlowInst,
        'createStockCashFlow': createStockCashFlow,
        'stockAdmInst': stockAdmInst,
        'figureUnitInst': figureUnitInst,
        'financialFigureUnitsCreate': financialFigureUnitsCreate,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'annualReportsDHRPInst': annualReportsDHRPInst,
        'annualReportsDHRPImageInst': annualReportsDHRPImage_serialized_data,
        'createAnnualReportsDHRP': createAnnualReportsDHRP,
        'createannualReportsDHRPImage': createannualReportsDHRPImage,
        'createStockBalanceSheetTTM': createStockBalanceSheetTTM,
        'balanceSheetTTMInst': balanceSheetTTMInst,
        'profitAndLossTTMInst': profitAndLossTTMInst,
        'createStockProfitAndLossTTM': createStockProfitAndLossTTM,
        'cashFlowTTMInst': cashFlowTTMInst,
        'createCashFlowTTM': createCashFlowTTM,
        'stockFinBalanceSheetSEOInst': stockFinBalanceSheetSEOInst,
        'createStockFinBalanceSheetSEO': createStockFinBalanceSheetSEO,
        'stockDeckAndDocsInst': stockDeckAndDocsInst,
        'stockDeckAndDocsInstForm': stockDeckAndDocsInstForm,
    }

    return render(request, 'UI/financial.html', context)


#
class crawledNewsSelfObj:
    def __init__(self, title=None, releaseDate_self=None, source_self=None, get_current_image=None,
                 get_absolute_url='javascript:void(0);'):
        self.title = title
        self.releaseDate_self = releaseDate_self
        self.source_self = source_self
        self.get_current_image = get_current_image
        self.get_absolute_url = get_absolute_url


# Creating object class
class newsClubbedObjects:
    def __init__(self, title=None, releaseDate_self=None, source_self=None, get_current_image=None,
                 get_absolute_url=None, completeObject=None):
        self.title = title
        if releaseDate_self:
            self.releaseDate_self = releaseDate_self
        else:
            self.releaseDate_self = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d').date()
        self.source_self = source_self
        self.get_current_image = get_current_image
        self.get_absolute_url = get_absolute_url
        self.completeObject = completeObject

    def __str__(self):
        return self.releaseDate_self

    class Meta:
        ordering = ['-releaseDate_self', ]


class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return dict(year=o.year, month=o.month, day=o.day)
        if isinstance(o, decimal.Decimal):
            return str(o)
        return o.__dict__


#
def newsView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    createStockNews = stockNewsForm()
    newsListRaw = {}
    websiteMasterInst = websiteMaster.objects.filter(stockProfileName=stock)
    createWebsiteMasters = websiteMasterForm()

    pageType = request.GET.get('type')
    newsDatalist = []
    if pageType == 'articles-only':
        stockNewsInst = stockNews.objects.filter(stockProfileName=stock, newsType='Articles-Only').order_by(
            '-newsPublishDate')
        newsArticles = blogArticles.objects.filter(relatedResearchReports=stock).order_by('-dateForListing')
        newsBlog = blogNews.objects.filter(relatedResearchReports=stock).order_by('-dateOfNews')
        for item in stockNewsInst:
            newsObj = newsClubbedObjects(item.title, item.newsPublishDate, item.source_self, item.get_current_image,
                                         item.get_absolute_url, item)
            newsDatalist.append(newsObj)
        for item in newsBlog:
            newsBlogObj = newsClubbedObjects(item.title, item.dateOfNews, 'News Blog', item.get_current_image,
                                             item.get_absolute_url)
            newsDatalist.append(newsBlogObj)
        for item in newsArticles:
            newsArticlesObj = newsClubbedObjects(item.title, item.dateForListing, 'Article Blog', item.articleImage,
                                                 item.get_absolute_url)
            newsDatalist.append(newsArticlesObj)
        with connections['cralwer'].cursor() as cursor:
            status = "'published'"
            SEOTitle = "'" + stock.seoTitle + "'"
            query = 'Select title, date, site, img, link from "crawlApp_googlenewsstore" where status=' + status + ' AND "connectedStock"=' + SEOTitle + ';'
            cursor.execute(query)
            newsListRaw = cursor.fetchall()
            for item in newsListRaw:
                newsLink = 'https://' + str(item[4])
                if item[3]:
                    imgLink = item[3]
                else:
                    imgLink = stock.logo.url
                crawledNewsSelf = newsClubbedObjects(item[0], item[1], item[2], imgLink, newsLink)
                newsDatalist.append(crawledNewsSelf)
    elif pageType == 'videos-only':
        stockNewsInst = stockNews.objects.filter(stockProfileName=stock, newsType='Videos-Only').order_by(
            '-newsPublishDate')
        newsVideoShorts = blogVideosShorts.objects.filter(relatedResearchReports=stock).order_by('-releaseDate')
        newsVideos = blogVideos.objects.filter(relatedResearchReports=stock).order_by('-releasedDate')
        for item in stockNewsInst:
            newsObj = newsClubbedObjects(item.title, item.newsPublishDate, item.source_self, item.get_current_image,
                                         item.get_absolute_url, item)
            newsDatalist.append(newsObj)
        for item in newsVideoShorts:
            if item.releaseDate:
                itemDate = item.releaseDate.date()
            else:
                itemDate = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d').date()
            shortsObj = newsClubbedObjects(item.title, itemDate, 'Shorts Blog', item.get_current_image,
                                           item.get_absolute_url)
            newsDatalist.append(shortsObj)
        for item in newsVideos:
            videosObj = newsClubbedObjects(item.title, item.releasedDate, 'Video Blog', item.get_current_image,
                                           item.get_absolute_url)
            newsDatalist.append(videosObj)
    else:
        newsBlog = blogNews.objects.filter(relatedResearchReports=stock).order_by('-dateOfNews')
        newsVideoShorts = blogVideosShorts.objects.filter(relatedResearchReports=stock).order_by('-releaseDate')
        newsVideos = blogVideos.objects.filter(relatedResearchReports=stock).order_by('-releasedDate')
        newsArticles = blogArticles.objects.filter(relatedResearchReports=stock).order_by('-dateForListing')
        stockNewsInst = stockNews.objects.filter(stockProfileName=stock).order_by('-newsPublishDate')
        for item in stockNewsInst:
            newsObj = newsClubbedObjects(item.title, item.newsPublishDate, item.source_self, item.get_current_image,
                                         item.get_absolute_url, item)
            newsDatalist.append(newsObj)
        for item in newsVideoShorts:
            if item.releaseDate:
                itemDate = item.releaseDate.date()
            else:
                itemDate = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d').date()
            shortsObj = newsClubbedObjects(item.title, itemDate, 'Shorts Blog', item.get_current_image,
                                           item.get_absolute_url)
            newsDatalist.append(shortsObj)
        for item in newsBlog:
            newsBlogObj = newsClubbedObjects(item.title, item.dateOfNews, 'News Blog', item.get_current_image,
                                             item.get_absolute_url)
            newsDatalist.append(newsBlogObj)
        for item in newsVideos:
            videosObj = newsClubbedObjects(item.title, item.releasedDate, 'Video Blog', item.get_current_image,
                                           item.get_absolute_url)
            newsDatalist.append(videosObj)
        for item in newsArticles:
            newsArticlesObj = newsClubbedObjects(item.title, item.dateForListing, 'Article Blog', item.articleImage,
                                                 item.get_absolute_url)
            newsDatalist.append(newsArticlesObj)
        with connections['cralwer'].cursor() as cursor:
            status = "'published'"
            SEOTitle = "'" + stock.seoTitle + "'"
            query = 'Select title, date, site, img, link from "crawlApp_googlenewsstore" where status=' + status + ' AND "connectedStock"=' + SEOTitle + ' order by date desc;'
            cursor.execute(query)
            newsListRaw = cursor.fetchall()
            for item in newsListRaw:
                newsLink = 'https://' + str(item[4])
                crawledNewsSelf = newsClubbedObjects(item[0], item[1], item[2], item[3], newsLink)
                newsDatalist.append(crawledNewsSelf)
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None
    despositoryOptions, saleType = rightSideMenuObjs()

    newsDatalist.sort(key=lambda x: x.releaseDate_self, reverse=True)

    # description field for SEO - starts
    try:
        stockNewsSEOInst = stockNewsSEO.objects.get(stockProfileName=stock)
    except:
        stockNewsSEOInst = None
    createStockNewsSEO = stockNewsSEOForm(instance=stockNewsSEOInst)
    # description field for SEO - ends
    try:
        newsVideosheadnews = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadnews = []

    try:
        typeofcompanyInstnews = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstnews = None

    context = {
        'stock': stock,
        'newsVideosheadnews': newsVideosheadnews,
        'typeofcompanyInstnews': typeofcompanyInstnews,
        'stockNewsInst': stockNewsInst,
        'createStockNews': createStockNews,
        'websiteMasterInst': websiteMasterInst,
        'createWebsiteMasters': createWebsiteMasters,
        'stockAdmInst': stockAdmInst,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'newsDatalist': newsDatalist,
        'newsListRaw': newsListRaw,
        'stockNewsSEOInst': stockNewsSEOInst,
        'createStockNewsSEO': createStockNewsSEO,
    }
    return render(request, 'UI/news.html', context)


#
def eventsView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None

    stockEventsDividendInst = stockEventsDividend.objects.filter(stockProfileName=stock).order_by('-exDateFrDividend')
    pastDividents = []
    futureDividents = []
    for item in stockEventsDividendInst:
        if str(item.exDateFrDividend) > today:
            futureDividents.append(item)
        else:
            pastDividents.append(item)
    createStockEventsDividend = stockEventsDividendForm()
    despositoryOptions, saleType = rightSideMenuObjs()
    stockEventsCorpActionsInst = stockEventsCorpActions.objects.filter(stockProfileName=stock).order_by(
        '-exDateFrCorporate')
    pastCorpActions = []
    futureCorpActions = []
    for item in stockEventsCorpActionsInst:
        if str(item.exDateFrCorporate) > today:
            futureCorpActions.append(item)
        else:
            pastCorpActions.append(item)
    createStockEventsCorpActions = stockEventsCorpActionsForm()

    stockEventsAnnouncementsInst = stockEventsAnnouncements.objects.filter(stockProfileName=stock).order_by(
        '-dateFrAnnouncement')
    pastAnnouncements = []
    futureAnnouncements = []
    for item in stockEventsAnnouncementsInst:
        if str(item.dateFrAnnouncement) > today:
            futureAnnouncements.append(item)
        else:
            pastAnnouncements.append(item)
    createStockEventsAnnouncements = stockEventsAnnouncementsForm()

    stockEventsLegalOrdersInst = stockEventsLegalOrders.objects.filter(stockProfileName=stock).order_by(
        '-exDateFrLegalOrders')
    createStockEventsLegalOrders = stockEventsLegalOrdersForm()

    # description field for SEO - starts
    try:
        stockEventsSEOInst = stockEventsSEO.objects.get(stockProfileName=stock)
    except:
        stockEventsSEOInst = None
    createStockEventsSEO = stockEventsSEOForm(instance=stockEventsSEOInst)
    # description field for SEO - ends
    try:
        newsVideosheadevents = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadevents = []

    try:
        typeofcompanyInstevents = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstevents = None

    context = {
        'stock': stock,
        'newsVideosheadevents': newsVideosheadevents,
        'typeofcompanyInstevents': typeofcompanyInstevents,
        'createStockEventsDividend': createStockEventsDividend,
        'createStockEventsCorpActions': createStockEventsCorpActions,
        'createStockEventsAnnouncements': createStockEventsAnnouncements,
        'createStockEventsLegalOrders': createStockEventsLegalOrders,
        'pastDividents': pastDividents,
        'futureDividents': futureDividents,
        'pastCorpActions': pastCorpActions,
        'futureCorpActions': futureCorpActions,
        'pastAnnouncements': pastAnnouncements,
        'futureAnnouncements': futureAnnouncements,
        'stockEventsLegalOrdersInst': stockEventsLegalOrdersInst,
        'stockAdmInst': stockAdmInst,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'stockEventsSEOInst': stockEventsSEOInst,
        'createStockEventsSEO': createStockEventsSEO,

    }
    return render(request, 'UI/events.html', context)


#
def stockBalanceSheetCalculation(stock):
    # balanceSheetSolvency = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('-year')[0:7]
    balanceSheetSolvency = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('-year')[0:10]
    blYearList = []
    deRatio = {}
    currentRatio = {}
    quickRatio = {}
    avgROceDenoPart = {}
    averageTotalEquityDict = {}
    avgTotalLongTermDebtDict = {}
    avgIntangibleAssetDict = {}
    avgTotalAssetDict = {}
    for item in balanceSheetSolvency:
        blYearList.append(item.year)
    yearListLen = len(blYearList)
    for i in range(yearListLen):
        if (i + 1) < yearListLen:
            CYear = blYearList[i]
            PYear = blYearList[i + 1]
            CYMain = stockBalanceSheet.objects.get(stockProfileName=stock, year=CYear)
            PYMain = stockBalanceSheet.objects.get(stockProfileName=stock, year=PYear)

            if CYMain.totalLongTermDebt:
                totalLnDebtCY = CYMain.totalLongTermDebt
            else:
                totalLnDebtCY = 0

            if PYMain.totalLongTermDebt:
                totalLnDebtPY = PYMain.totalLongTermDebt
            else:
                totalLnDebtPY = 0

            if CYMain.currentPortionOfLongTermDebt:
                currPortLnTermDebtCY = CYMain.currentPortionOfLongTermDebt
            else:
                currPortLnTermDebtCY = 0

            if PYMain.currentPortionOfLongTermDebt:
                currPortLnTermDebtPY = PYMain.currentPortionOfLongTermDebt
            else:
                currPortLnTermDebtPY = 0

            if CYMain.currentPortionOfLeases:
                currPortLeasesCY = CYMain.currentPortionOfLeases
            else:
                currPortLeasesCY = 0

            if PYMain.currentPortionOfLeases:
                currPortLeasesPY = PYMain.currentPortionOfLeases
            else:
                currPortLeasesPY = 0

            if CYMain.longTermPortionOfLeases:
                lnTermPortionOfLeasesCY = CYMain.longTermPortionOfLeases
            else:
                lnTermPortionOfLeasesCY = 0

            if PYMain.longTermPortionOfLeases:
                lnTermPortionOfLeasesPY = PYMain.longTermPortionOfLeases
            else:
                lnTermPortionOfLeasesPY = 0

            if CYMain.totalEquity:
                totalEquityCY = CYMain.totalEquity
            else:
                totalEquityCY = 0
            if PYMain.totalEquity:
                totalEquityPY = PYMain.totalEquity
            else:
                totalEquityPY = 0

            if CYMain.currentAssets:
                currentAssetsCY = CYMain.currentAssets
            else:
                currentAssetsCY = 0
            if PYMain.currentAssets:
                currentAssetsPY = PYMain.currentAssets
            else:
                currentAssetsPY = 0
            if CYMain.currentLiabilities:
                currentLiabCY = CYMain.currentLiabilities
            else:
                currentLiabCY = 0
            if PYMain.currentLiabilities:
                currentLiabPY = PYMain.currentLiabilities
            else:
                currentLiabPY = 0
            if CYMain.nonCurrentLiabilities:
                nonCurrentLiabCY = CYMain.nonCurrentLiabilities
            else:
                nonCurrentLiabCY = 0
            if PYMain.nonCurrentLiabilities:
                nonCurrentLiabPY = PYMain.nonCurrentLiabilities
            else:
                nonCurrentLiabPY = 0
            if CYMain.totalInventory:
                totInvCY = CYMain.totalInventory
            else:
                totInvCY = 0
            if PYMain.totalInventory:
                totInvPY = PYMain.totalInventory
            else:
                totInvPY = 0
            if CYMain.prepaidExpenses:
                prepaidExpCY = CYMain.prepaidExpenses
            else:
                prepaidExpCY = 0
            if PYMain.prepaidExpenses:
                prepaidExpPY = PYMain.prepaidExpenses
            else:
                prepaidExpPY = 0
            if CYMain.nonCurrentAssets:
                nonCurrentAssetsCY = CYMain.nonCurrentAssets
            else:
                nonCurrentAssetsCY = 0
            if PYMain.nonCurrentAssets:
                nonCurrentAssetsPY = PYMain.nonCurrentAssets
            else:
                nonCurrentAssetsPY = 0
            if CYMain.otherIntangibleAssests:
                othrIntangAssestsCY = CYMain.otherIntangibleAssests
            else:
                othrIntangAssestsCY = 0
            if PYMain.otherIntangibleAssests:
                othrIntangAssestsPY = PYMain.otherIntangibleAssests
            else:
                othrIntangAssestsPY = 0

            totalCalculatedLnDebtCY = totalLnDebtCY + currPortLnTermDebtCY + currPortLeasesCY + lnTermPortionOfLeasesCY
            totalCalculatedLnDebtPY = totalLnDebtPY + currPortLnTermDebtPY + currPortLeasesPY + lnTermPortionOfLeasesPY

            avgCalculatedNonLiabilities = (nonCurrentLiabCY + nonCurrentLiabPY) / Decimal(2)
            avgTotalLongTermDebt = (totalCalculatedLnDebtCY + totalCalculatedLnDebtPY) / Decimal(2)
            avgTotalEquity = (totalEquityCY + totalEquityPY) / Decimal(2)
            avgCurrentAsset = (currentAssetsCY + currentAssetsPY) / Decimal(2)
            avgNonCurrentAsset = (nonCurrentAssetsCY + nonCurrentAssetsPY) / Decimal(2)
            avgCurrentLiabilities = (currentLiabCY + currentLiabPY) / Decimal(2)
            avgInventory = (totInvCY + totInvPY) / Decimal(2)
            avgPrepaidExpenses = (prepaidExpCY + prepaidExpPY) / Decimal(2)
            avgIntangibleAsset = (othrIntangAssestsCY + othrIntangAssestsPY) / Decimal(2)

            if avgTotalEquity == 0:
                avgTotalEquity = 1

            if avgCurrentLiabilities == 0:
                avgCurrentLiabilities = 1

            deRatio[CYear] = round((avgTotalLongTermDebt / avgTotalEquity), 2)
            currentRatio[CYear] = round((avgCurrentAsset / avgCurrentLiabilities), 2)
            quickRatio[CYear] = round(((avgCurrentAsset - avgInventory + avgPrepaidExpenses) / avgCurrentLiabilities),
                                      2)

            # changes related to Kulmehar report starts
            # averageTotalEquityDict[CYear] = round(avgTotalEquity,2)
            # changes related to Kulmehar report ends

            averageTotalEquityDict[CYear] = avgTotalEquity

            avgTotalLongTermDebtDict[CYear] = round(avgTotalLongTermDebt, 2)

            # changes related to Kulmehar report starts
            # avgTotalAssetDict[CYear] = round(avgCurrentAsset + avgNonCurrentAsset,2)
            # changes related to Kulmehar report ends

            avgTotalAssetDict[CYear] = avgCurrentAsset + avgNonCurrentAsset

            # changes related to Kulmehar report starts
            # avgIntangibleAssetDict[CYear] = round(avgIntangibleAsset,2)
            # changes related to Kulmehar report ends

            avgIntangibleAssetDict[CYear] = avgIntangibleAsset

            # Ishima ROCE formula denominator changes starts
            # avgROceDenoPart[CYear] = round(avgCalculatedNonLiabilities,2)
            avgROceDenoPart[CYear] = round(avgCurrentLiabilities, 2)
        # Ishima ROCE formula denominator changes ends

    return deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgIntangibleAssetDict, avgROceDenoPart


#
def stockProfitAndLossCalculation(stock, callingFunction=0):
    interestCoverageRatio = {}
    operatingProfitEBITmargin = {}
    pbtMargin = {}
    patMargin = {}
    netIncomeDict = {}
    netIncomeSnapShotDict = {}
    pbitDict = {}
    revenueDict = {}
    # profitLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')[0:7]
    profitLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    forCount = 0
    for item in profitLoss:
        forCount += 1
        if item.pbit:
            pbitCal = item.pbit
        else:
            pbitCal = 1
        if item.interestExpense:
            interestExpCal = item.interestExpense
        else:
            interestExpCal = 1
        if item.totalRevenue:
            totalRevenueCal = item.totalRevenue
        else:
            totalRevenueCal = 1
        if item.revenue:
            revenueOnlyCal = item.revenue
        else:
            revenueOnlyCal = 1
        if item.pbt:
            pbtCal = item.pbt
        else:
            pbtCal = 1
        if item.netIncome:
            netIncomeCal = item.netIncome
        else:
            netIncomeCal = 1
        if item.totalRevenue:
            revenueCal = item.totalRevenue
        else:
            revenueCal = 1

        interestCoverageRatio[item.year] = round((pbitCal / interestExpCal), 2)
        operatingProfitEBITmargin[item.year] = round((pbitCal / revenueOnlyCal) * 100, 2)
        pbtMargin[item.year] = round((pbtCal / revenueOnlyCal) * 100, 2)
        patMargin[item.year] = round((netIncomeCal / revenueOnlyCal) * 100, 2)
        # changes from Kulmeher report starts
        # netIncomeDict[item.year] = round(netIncomeCal,2)
        # changes from Kulmeher report ends
        netIncomeDict[item.year] = netIncomeCal

        netIncomeSnapShotDict[forCount] = round(netIncomeCal, 2)
        pbitDict[item.year] = round(pbitCal, 2)
        revenueDict[item.year] = round(revenueCal, 2)
    if callingFunction == 'snapshot':
        return revenueDict, netIncomeSnapShotDict
    else:
        return interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict


# --> Old calculateProgrammedGrowth Function
# def calculateProgrammedGrowth(growthDict):
# 	temp2Key = None
# 	tempFor2 = None
# 	temp3Key = None
# 	tempFor3 = None
# 	lenOFDict = len(growthDict)
# 	processedDict = {}
# 	if 0 < lenOFDict <= 3:
# 		processedDict = growthDict
# 	elif lenOFDict == 4:
# 		forCount = 1
# 		tempFor2 = None
# 		tempFor3 = None
# 		# get 1, (best of 2,3) and 4
# 		for key, val in growthDict.items():
# 			if forCount == 2 or forCount == 3:
# 				if forCount == 2:
# 					temp2Key = forCount
# 					tempFor2 = val
# 				if forCount == 3:
# 					temp3Key = forCount
# 					tempFor3 = val
# 				if tempFor2 and tempFor3:
# 					if return_number_or_0(tempFor2) > return_number_or_0(tempFor3):
# 						processedDict[temp2Key] = tempFor2
# 					else:
# 						processedDict[temp3Key] = tempFor3
# 			else:
# 				processedDict[forCount] = val
# 			forCount += 1
# 	elif lenOFDict > 4:
# 		forCount = 1
# 		for key, val in growthDict.items():
# 			if forCount == 1 or forCount == 3 or forCount == 5:
# 				processedDict[forCount] = val
# 			forCount += 1
# 	return processedDict

# -->New calculateProgrammedGrowth Function to fix the value growth showing !!
def calculateProgrammedGrowth(growthDict):
	temp2Key = None
	tempFor2 = None
	temp3Key = None
	tempFor3 = None
	lenOFDict = len(growthDict)
	processedDict = {}
	if 0 < lenOFDict <= 3:
		processedDict = growthDict
	elif lenOFDict == 4:
		forCount = 1
		tempFor2 = None
		tempFor3 = None
		# get 1, (best of 2,3) and 4
		for key, val in growthDict.items():
			if forCount == 2 or forCount == 3:
				if forCount == 2:
					temp2Key = forCount
					tempFor2 = val
				if forCount == 3:
					temp3Key = forCount
					tempFor3 = val
				if tempFor2 and tempFor3:
					if return_number_or_0(tempFor2) > return_number_or_0(tempFor3):
						processedDict[temp2Key] = tempFor2
					else:
						processedDict[temp3Key] = tempFor3
			else:
				processedDict[forCount] = val
			forCount += 1
	elif lenOFDict > 4:
		forCount = 1
		tempKey = 1
		tempVal = 1
		for key, val in growthDict.items():
			midValues = lenOFDict//2
			if forCount == 1 or forCount == lenOFDict:
				processedDict[forCount] = val
			elif forCount == midValues:
				tempKey = forCount
				tempVal = val

			elif forCount == midValues + 1:
				# print(growthDict)
				# print(tempVal)
				# print(val)
				if val >= tempVal :
					processedDict[forCount] = val
					# print("upcomming val is greater")
					# print(val)
				else:
					processedDict[tempKey] = tempVal
					# print("upcomming val is smaller")
					# print(tempVal)
			else:
				pass
			forCount += 1	
			# print(processedDict)	
	return processedDict

	# old logic for calculateProgrammedGrowth ----->
	#  
	# 	forCount = 1
	# 	for key, val in growthDict.items():
	# 		midGrowth = lenOFDict//2
	# 		if forCount == 1 or forCount == lenOFDict:
	# 			processedDict[forCount] = val
	# 		elif forCount in [midGrowth, midGrowth-1, midGrowth+1]:
	# 			midGrowthList = []
	# 			midGrowthList.append(val)
	# 			minMidGrowthKey = forCount
	# 			minMidGrowthVal = val
	# 			if val < min(midGrowthList):
	# 				minMidGrowthKey = forCount
	# 				minMidGrowthVal = val
	# 		elif forCount > (midGrowth + 1):
	# 			processedDict[minMidGrowthKey] = minMidGrowthVal
	# 		forCount += 1	
	# return processedDict



#
# def growthCalculatorForAnnualValues(stock, growthFor='bookValue'):
#     if growthFor == 'bookValue':
#         objs = bookValueData.objects.filter(stockProfileName=stock).order_by('-year')[0:7]
#     elif growthFor == 'assetGrowth':
#         objs = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('-year')[0:7]
#     elif growthFor == 'cashFlow':
#         objs = stockCashFlow.objects.filter(stockProfileName=stock).order_by('-year')[0:7]
#     valDict = {}
#     valDictFinancing = {}
#     totalYearsData = []
#     for item in objs:
#         totalYearsData.append(item.year)
#     if (len(totalYearsData) > 1):
#         CYear = totalYearsData[0]
#         if growthFor == 'bookValue':
#             CY = bookValueData.objects.get(stockProfileName=stock, year=CYear)
#         elif growthFor == 'assetGrowth':
#             CY = stockBalanceSheet.objects.get(stockProfileName=stock, year=CYear)
#         elif growthFor == 'cashFlow':
#             CY = stockCashFlow.objects.get(stockProfileName=stock, year=CYear)
#     for i, j in enumerate(totalYearsData[:-1]):
#         forloopCounter = i + 1
#         firstYear = j
#         prevYear = totalYearsData[i + 1]
#         n = CYear - prevYear
#         if growthFor == 'bookValue':
#             PY = bookValueData.objects.get(stockProfileName=stock, year=prevYear)
#             calculatedValGrowth = calGrowthFormulaView(CY.bookValue, PY.bookValue, n)
#         elif growthFor == 'assetGrowth':
#             PY = stockBalanceSheet.objects.get(stockProfileName=stock, year=prevYear)
#             calculatedValGrowth = calGrowthFormulaView(CY.totalAssets, PY.totalAssets, n)
#         elif growthFor == 'cashFlow':
#             PY = stockCashFlow.objects.get(stockProfileName=stock, year=prevYear)
#             calculatedValGrowth = calGrowthFormulaView(CY.cashFromOperatingActivities, PY.cashFromOperatingActivities,
#                                                        n)
#             calculatedValGrowthFinancing = calGrowthFormulaView(CY.cashFromFinancingActivities,
#                                                                 PY.cashFromFinancingActivities, n)
#         if calculatedValGrowth:
#             valDict[forloopCounter] = calculatedValGrowth
#         if growthFor == 'cashFlow':
#             valDictFinancing[forloopCounter] = calculatedValGrowthFinancing
#     processedDict = calculateProgrammedGrowth(valDict)
#     if growthFor == 'cashFlow':
#         processedDictFinancing = calculateProgrammedGrowth(valDictFinancing)
#         return processedDict, processedDictFinancing
#     else:
#         return processedDict


def growthCalculatorForAnnualValues(stock, growthFor='bookValue'):
	if growthFor == 'bookValue':
		objs = bookValueData.objects.filter(stockProfileName = stock).order_by('-year')[0:]
	elif growthFor == 'assetGrowth':
		objs = stockBalanceSheet.objects.filter(stockProfileName = stock).order_by('-year')[0:]
	elif growthFor == 'cashFlow':
		objs = stockCashFlow.objects.filter(stockProfileName = stock).order_by('-year')[0:]

	valDict = {}
	valDictFinancing = {}
	totalYearsData = []
	for item in objs:
		totalYearsData.append(item.year)
	# print(totalYearsData)
	if (len(totalYearsData) > 1):
		CYear = totalYearsData[0]
		# for item in bookValuesObjs:
		# 	try:
		# 		totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=item.year)
		# 		totalShareOutstanding = totalShareOutStandValueObj.totalCommonSharesOutstanding
		# 		newBookValue = item.bookValue / totalShareOutstanding
		# 		bookValues[item.year] = newBookValue
		# 	except:
		# 		pass		
		if growthFor == 'bookValue':
			CY = bookValueData.objects.get(stockProfileName=stock, year=CYear)
		elif growthFor == 'assetGrowth':
			CY = stockBalanceSheet.objects.get(stockProfileName=stock, year=CYear)
		elif growthFor == 'cashFlow':
			CY = stockCashFlow.objects.get(stockProfileName=stock, year=CYear)
	totalShareOutstanding = {}
	bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('-year')[0:]
	for item in bookValuesObjs:
		totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=item.year)
		totalShareOutstanding[item.year] = totalShareOutStandValueObj.totalCommonSharesOutstanding
	for i, j in enumerate(totalYearsData[:-1]):
		forloopCounter = i + 1
		firstYear = j
		prevYear = totalYearsData[i + 1]
		n = CYear - prevYear
		if growthFor == 'bookValue':
			PY = bookValueData.objects.get(stockProfileName=stock, year=prevYear)
			calculatedValGrowth = calGrowthFormulaView((CY.bookValue/totalShareOutstanding[CY.year]), (PY.bookValue/totalShareOutstanding[PY.year]), n)
			# PY = bookValueData.objects.get(stockProfileName=stock, year=prevYear)
			# calculatedValGrowth = calGrowthFormulaView((CY.bookValue/totalShareOutstanding), (PY.bookValue/totalShareOutstanding), n)
		elif growthFor == 'assetGrowth':
			PY = stockBalanceSheet.objects.get(stockProfileName=stock, year=prevYear)
			calculatedValGrowth = calGrowthFormulaView(CY.totalAssets, PY.totalAssets, n)
		elif growthFor == 'cashFlow':
			PY = stockCashFlow.objects.get(stockProfileName=stock, year=prevYear)
			calculatedValGrowth = calGrowthFormulaView(CY.cashFromOperatingActivities, PY.cashFromOperatingActivities,
													   n)
			calculatedValGrowthFinancing = calGrowthFormulaView(CY.cashFromFinancingActivities,
																PY.cashFromFinancingActivities, n)
		if calculatedValGrowth:
			valDict[forloopCounter] = calculatedValGrowth
		if growthFor == 'cashFlow':
			valDictFinancing[forloopCounter] = calculatedValGrowthFinancing
	processedDict = calculateProgrammedGrowth(valDict)
	if growthFor == 'cashFlow':
		processedDictFinancing = calculateProgrammedGrowth(valDictFinancing)
		return processedDict, processedDictFinancing
	else:
		return processedDict


#
def sortingDictLowToHigh(sortDict):
    dictYears = []
    processedDict = {}
    for key in sortDict.keys():
        dictYears.append(key)
    dictYears.sort()
    for item in dictYears:
        processedDict[item] = sortDict[item]
    return processedDict


#
def dividentYieldGraphView(divident=None, CMP=None):
    if divident == None or divident == 0 or CMP == None or CMP == 0:
        dividentYieldVal = False
    else:
        dividentYieldVal = round((divident / CMP) * 100, 2)
    return dividentYieldVal


#
def earningYieldGraphView(eps=None, CMP=None):
    if eps == None or eps == 0 or CMP == None or CMP == 0:
        earningYieldVal = False
    else:
        earningYieldVal = round((eps / CMP) * 100, 2)
    return earningYieldVal


#
def keyRatioView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
    if renderBankNBFCsTemplates:
        return keyRatioForBankNBFCsView(request, slug)
    stockProfitLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    balanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    cashFlow = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgIntangibleAssetDict, avgROceDenoPart = stockBalanceSheetCalculation(
        stock)
    interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict = stockProfitAndLossCalculation(
        stock)
    returnOnEquity = {}
    roce = {}
    returnOnAssets = {}
    dividentYield = {}
    earningYield = {}
    for key, val in netIncomeDict.items():
        val2 = averageTotalEquityDict.get(key)
        if val2:
            valEquity = val2
        else:
            valEquity = 1

        catROERounded = round((val / valEquity) * 100, 2)
        returnOnEquity[key] = catROERounded
    for item in stockProfitLoss:
        currentStockPrice = localOrScreenerPriceView(stock)
        # try:
        # 	currentStockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
        # 	currentStockPrice = currentStockPriceInst.investorPrice
        # except:
        # 	currentStockPrice = 0
        # divident
        try:
            DPSforThisYear = item.DPS
        except:
            DPSforThisYear = None
        calDividentforThisYear = dividentYieldGraphView(DPSforThisYear, currentStockPrice)
        if calDividentforThisYear:
            dividentYield[item.year] = calDividentforThisYear
        # earning
        calEPSforThisYear = check_eps_basic_or_diluted(item.basicEPS, item.dilutedEPS)
        calEarningforThisYear = earningYieldGraphView(calEPSforThisYear, currentStockPrice)
        if calEarningforThisYear:
            earningYield[item.year] = calEarningforThisYear

    # Ishima pointers changes for ROCE starts
    # for key, val in pbitDict.items():
    # 	val2 = averageTotalEquityDict.get(key)
    # 	val3 = avgROceDenoPart.get(key)
    # 	avgROceDenoPart
    # 	if val2:
    # 		valAverageEquity = val2
    # 	else :
    # 		valAverageEquity = 0

    # 	if val3:
    # 		valNonCurrentLiab = val3
    # 	else :
    # 		valNonCurrentLiab = 0

    # sumofEquityAndNonCrrLiabilities = valAverageEquity + valNonCurrentLiab
    # if not sumofEquityAndNonCrrLiabilities:
    # 	sumofEquityAndNonCrrLiabilities = 1
    # roce[key] = round((val / ( sumofEquityAndNonCrrLiabilities )) * 100,2)
    # Ishima pointers changes for ROCE ends

    for key, val in pbitDict.items():
        val2 = avgTotalAssetDict.get(key)
        val3 = avgROceDenoPart.get(key)
        avgROceDenoPart
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0

        if val3:
            valCurrentLiab = val3
        else:
            valCurrentLiab = 0

        sumofAssestAndCrrLiabilities = valAverageAsset - valCurrentLiab
        if not sumofAssestAndCrrLiabilities:
            sumofAssestAndCrrLiabilities = 1
        roce[key] = round((val / (sumofAssestAndCrrLiabilities)) * 100, 2)

    for key, val in netIncomeDict.items():
        val2 = avgTotalAssetDict.get(key)
        val3 = avgIntangibleAssetDict.get(key)
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0
        if val3:
            valAverageIntangibleAsset = val3
        else:
            valAverageIntangibleAsset = 0
        # processedVal = valAverageAsset - valAverageIntangibleAsset

        # changes from Kulmehar starts
        processedVal = valAverageAsset
        # chnages from Kulmehar ends

        if processedVal == 0:
            processedVal = 1

        returnOnAssets[key] = round((val / processedVal) * 100, 2)

    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None

    try:
        stockGrowthInst = stockGrowth.objects.get(stockProfileName=stock)
    except:
        stockGrowthInst = None
    createStockGrowth = stockGrowthForm(instance=stockGrowthInst)
    try:
        stockSolvencyInst = stockSolvency.objects.get(stockProfileName=stock)
    except:
        stockSolvencyInst = None
    createStockSolvency = stockSolvencyForm(instance=stockSolvencyInst)
    try:
        stockOperatingEfficiencyInst = stockOperatingEfficiency.objects.get(stockProfileName=stock)
    except:
        stockOperatingEfficiencyInst = None
    createStockOperatingEfficiency = stockOperatingEfficiencyForm(instance=stockOperatingEfficiencyInst)

    try:
        sectorSpecificRatiosInst = sectorSpecificRatios.objects.get(stockProfileName=stock)
    except:
        sectorSpecificRatiosInst = None
    createSectorSpecificRatios = sectorSpecificRatiosForm(instance=sectorSpecificRatiosInst)

    try:
        stockRatiosInst = stockRatios.objects.get(stockProfileName=stock)
    except:
        stockRatiosInst = None

    despositoryOptions, saleType = rightSideMenuObjs()
    createStockRatios = stockRatiosForm(instance=stockRatiosInst)
    returnedGrowthDataRevenue, returnedRevenueGrowthAlgoProgrammedData, returnedNetProfitGrowthData, returnedNetProfitAlgoProgrammedData, returnedEPSGrowthData, returnedEPSAlgoProgrammedData, returnedEBITDAGrowthData, returnedEBITDAAlgoProgrammedData, returnedPBITGrowthData, returnedPBITAlgoProgrammedData = calGrowthTemplateDataView(
        stock)
    processedRevenueGrowthTextual = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    processedNetProfitGrowthTextual = calculateProgrammedGrowth(returnedNetProfitAlgoProgrammedData)
    processedEPSGrowthTextual = calculateProgrammedGrowth(returnedEPSAlgoProgrammedData)
    processedEBITDAGrowthTextual = calculateProgrammedGrowth(returnedEBITDAAlgoProgrammedData)
    processedPBITGrowthTextual = calculateProgrammedGrowth(returnedPBITAlgoProgrammedData)
    processedBookValueGrowthTextual = growthCalculatorForAnnualValues(stock, growthFor='bookValue')
    processedAssetGrowthTextual = growthCalculatorForAnnualValues(stock, growthFor='assetGrowth')
    processedCashFlowGrowthTextual, processedCashFlowGrowthFinancingTextual = growthCalculatorForAnnualValues(stock,
                                                                                                              growthFor='cashFlow')

    indusSpecificGraphs = industrySpecificGraphs.objects.filter(stockProfileName=stock)
    industrySpecificGraph = industrySpecificGraphForm()

    industrySpecificValsGraph = industrySpecificGraphValsForm()
    indusGraphDict = {}
    for graph in indusSpecificGraphs:
        # indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:7]
        indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:10]
        # indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('-year')[0:7]
        indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by(
            '-year')[0:10]
        graphDict = {}
        dataDict = {}
        growthGraphDict = {}
        forCount = 0
        if graph.graphType == 'Value':
            graphDict['type'] = 'Value'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                forCount += 1
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
            for yearlyItemsGrowth in indusSpecificValsGraphsForGrowth:
                growthGraphDict[yearlyItemsGrowth.year] = yearlyItemsGrowth.value
            yearIs = 'key'
            requestFrom = 'keyRatioIndusSpecific'
            processedGrowthData = processDictForGrowthFormula(growthGraphDict, yearIs, requestFrom)
            growthData = calculateProgrammedGrowth(processedGrowthData)
            graphDict['growth'] = growthData
        else:
            graphDict['type'] = 'Percentage'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
        graphDict['data'] = dataDict
        graphDict['id'] = graph.id
        graphDict['description'] = graph.graphDescription
        indusGraphDict[graph.graphFor] = graphDict
    processedDeRatio = sortingDictLowToHigh(deRatio)
    processedCurrentRatio = sortingDictLowToHigh(currentRatio)
    processedQuickRatio = sortingDictLowToHigh(quickRatio)
    bookValues = {}
    bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    for item in bookValuesObjs:
        try:
            totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=item.year)
            totalShareOutstanding = totalShareOutStandValueObj.totalCommonSharesOutstanding
            newBookValue = item.bookValue / totalShareOutstanding
            bookValues[item.year] = newBookValue
        except:
            pass

    bookValuestoEdit = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    createBookValue = bookValueDataForm()

    #
    try:
        valuationRatioInst = valuationRatio.objects.latest('id')
    except:
        valuationRatioInst = None
    valuationRatioInstForm = valuationRatioForm(instance=valuationRatioInst)
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
    except:
        iDescriptionForKeyRatiosInst = None

    try:
        valuationRatioInst = valuationRatio.objects.latest('id')
    except:
        valuationRatioInst = None
    valuationRatioInstForm = valuationRatioForm(instance=valuationRatioInst)
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
    except:
        iDescriptionForKeyRatiosInst = None
    try:
        newsVideosheadkeyratio = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadkeyratio = []

    try:
        typeofcompanyInstkeyratio = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstkeyratio = None

    context = {
        'stock': stock,
        'stockProfitLoss': stockProfitLoss,
        'newsVideosheadkeyratio': newsVideosheadkeyratio,
        'typeofcompanyInstkeyratio': typeofcompanyInstkeyratio,
        'stockBalanceSheet': balanceSheet,
        'cashFlow': cashFlow,
        'stockGrowthInst': stockGrowthInst,
        'createStockGrowth': createStockGrowth,
        'stockSolvencyInst': stockSolvencyInst,
        'createStockSolvency': createStockSolvency,
        'stockOperatingEfficiencyInst': stockOperatingEfficiencyInst,
        'createStockOperatingEfficiency': createStockOperatingEfficiency,
        'sectorSpecificRatiosInst': sectorSpecificRatiosInst,
        'createSectorSpecificRatios': createSectorSpecificRatios,
        'stockRatiosInst': stockRatiosInst,
        'createStockRatios': createStockRatios,
        'deRatio': processedDeRatio,
        'currentRatio': processedCurrentRatio,
        'quickRatio': processedQuickRatio,
        'interestCoverageRatio': interestCoverageRatio,
        'operatingProfitEBITmargin': operatingProfitEBITmargin,
        'pbtMargin': pbtMargin,
        'patMargin': patMargin,
        'returnOnEquity': returnOnEquity,
        'roce': roce,
        'returnOnAssets': returnOnAssets,
        'returnedGrowthDataRevenue': returnedGrowthDataRevenue,
        'returnedNetProfitGrowthData': returnedNetProfitGrowthData,
        'returnedEPSGrowthData': returnedEPSGrowthData,
        'returnedEBITDAGrowthData': returnedEBITDAGrowthData,
        'returnedPBITGrowthData': returnedPBITGrowthData,
        'processedRevenueGrowthTextual': processedRevenueGrowthTextual,
        'processedNetProfitGrowthTextual': processedNetProfitGrowthTextual,
        'processedEPSGrowthTextual': processedEPSGrowthTextual,
        'processedEBITDAGrowthTextual': processedEBITDAGrowthTextual,
        'processedPBITGrowthTextual': processedPBITGrowthTextual,
        'processedBookValueGrowthTextual': processedBookValueGrowthTextual,
        'processedAssetGrowthTextual': processedAssetGrowthTextual,
        'processedCashFlowGrowthTextual': processedCashFlowGrowthTextual,
        'processedCashFlowGrowthFinancingTextual': processedCashFlowGrowthFinancingTextual,
        'industrySpecificGraph': industrySpecificGraph,
        'industrySpecificValsGraph': industrySpecificValsGraph,
        'indusGraphDict': indusGraphDict,
        'createBookValue': createBookValue,
        'bookValues': bookValues,
        'stockAdmInst': stockAdmInst,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'bookValuestoEdit': bookValuestoEdit,
        'dividentYield': dividentYield,
        'earningYield': earningYield,
        'valuationRatioInst': valuationRatioInst,
        'valuationRatioInstForm': valuationRatioInstForm,
        'iDescriptionForKeyRatiosInst': iDescriptionForKeyRatiosInst,
    }
    return render(request, 'UI/keyRatio.html', context)


#
def netProfitMarginFormula(PAT=0.00, totalRevenue=1.00):
    if PAT == None:
        PAT = 0.00
    if totalRevenue == None or totalRevenue == 0:
        totalRevenue = 1.00
    nPMF = (Decimal(PAT) / Decimal(totalRevenue)) * 100
    return nPMF


#
def totalAssetTurnoverRatioFormula(revenue=0.00, totalAssetCY=0.00, totalAssetPY=0.00):
    if totalAssetCY == None:
        totalAssetCY = 0.00
    if totalAssetPY == None:
        totalAssetPY = 0.00
    totalAssetPlus = Decimal(totalAssetCY) + Decimal(totalAssetPY)
    totalAssetAvg = Decimal(totalAssetPlus) / Decimal(2.00)
    if totalAssetAvg == 0.00 or totalAssetAvg == None:
        totalAssetAvg = 1.00
    totalAssetTurnoverRatio = Decimal(revenue) / Decimal(totalAssetAvg)
    return totalAssetTurnoverRatio


#
#
def totalFixedAssetTurnoverRatioFormula(revenue=0.00, totalInvCY=0.00,
                                        totalInvPY=0.00):  # this formula is calculating Inventory Turn Over ratio.
    totalInvPlus = Decimal(totalInvCY) + Decimal(totalInvPY)
    totalInventoryAverage = Decimal(totalInvPlus) / Decimal(2)
    if totalInventoryAverage == 0.00 or totalInventoryAverage == None:
        totalInventoryAverage = 1.00
    totalFixedAssetTurnoverRatio = Decimal(revenue) / Decimal(totalInventoryAverage)
    return totalFixedAssetTurnoverRatio


# def totalFixedAssetTurnoverRatioFormula(revenue=0.00,totalAssetCY=0.00,totalAssetPY=0.00,intangibleAssetCY=0.00,intangibleAssetPY=0.00):
# 	if totalAssetCY == None:
# 		totalAssetCY = 0.00
# 	if totalAssetPY == None:
# 		totalAssetPY = 0.00
# 	if intangibleAssetCY == None:
# 		intangibleAssetCY = 0.00
# 	if intangibleAssetPY == None:
# 		intangibleAssetPY = 0.00
# 	totalAssetPlus = Decimal(totalAssetCY) + Decimal(totalAssetPY)
# 	totalAssetAvg = Decimal(totalAssetPlus) / Decimal(2.00)
# 	totalIntangibleAssetPlus = Decimal(intangibleAssetCY) + Decimal(intangibleAssetPY)
# 	totalIntangibleAssetAvg = Decimal(totalIntangibleAssetPlus) / Decimal(2.00)
# 	processedData = Decimal(totalAssetAvg) - Decimal(totalIntangibleAssetAvg)
# 	if processedData == 0 or processedData == None:
# 		processedData = 1.00
# 	totalFixedAssetTurnoverRatio = Decimal(revenue) / Decimal(processedData) * 100
# 	return totalFixedAssetTurnoverRatio

#
def ROEFormula(netIncome=0.00, totalEquityCY=0.00, totalEquityPY=0.00):
    if totalEquityCY == None:
        totalEquityCY = 0.00
    if totalEquityPY == None:
        totalEquityPY = 0.00
    if netIncome == None:
        netIncome = 0.00
    totalEquityPlus = Decimal(totalEquityCY) + Decimal(totalEquityPY)
    totalEquityAvg = Decimal(totalEquityPlus) / Decimal(2)
    if totalEquityAvg == 0 or totalEquityAvg == None:
        totalEquityAvg = 1
    ROE = (Decimal(netIncome) / Decimal(totalEquityAvg)) * 100
    return ROE


#
def ROCEFormula(EBIT=0, totalEquityCY=0, totalEquityPY=0, totalNonCurrentLiabilityCY=0.00,
                totalNonCurrentLiabilityPY=0.00):
    if totalEquityCY == None:
        totalEquityCY = 0.00
    if totalEquityPY == None:
        totalEquityPY = 0.00
    if totalNonCurrentLiabilityCY == None:
        totalNonCurrentLiabilityCY = 0.00
    if totalNonCurrentLiabilityPY == None:
        totalNonCurrentLiabilityPY = 0.00

    totalEquityPlus = Decimal(totalEquityCY) + Decimal(totalEquityPY)
    totalEquityAvg = Decimal(totalEquityPlus) / Decimal(2.00)

    totalNonCurrentLiabilitiesPlus = Decimal(totalNonCurrentLiabilityCY) + Decimal(totalNonCurrentLiabilityPY)
    totalNonCurrentLiabilitiesAvg = Decimal(totalNonCurrentLiabilitiesPlus) / Decimal(2.00)

    processedData = Decimal(totalEquityAvg) + Decimal(totalNonCurrentLiabilitiesAvg)
    if processedData == 0 or processedData == None:
        processedData = 1
    ROCE = (Decimal(EBIT) / Decimal(processedData)) * 100
    return ROCE


# #
# def ROCEFormula(EBIT=0,totalEquityCY=0,totalEquityPY=0,longTermDebtCY=0,longTermDebtPY=0):
# 	if totalEquityCY == None:
# 		totalEquityCY = 0.00
# 	if totalEquityPY == None:
# 		totalEquityPY = 0.00
# 	if longTermDebtCY == None:
# 		longTermDebtCY = 0.00
# 	if longTermDebtPY == None:
# 		longTermDebtPY = 0.00
# 	totalEquityPlus = Decimal(totalEquityCY) + Decimal(totalEquityPY)
# 	totalEquityAvg = Decimal(totalEquityPlus) / Decimal(2.00)
# 	longTermDebtPlus = Decimal(longTermDebtCY) + Decimal(longTermDebtPY)
# 	longTermDebtAvg = Decimal(longTermDebtPlus) / Decimal(2.00)
# 	processedData = Decimal(totalEquityAvg) + Decimal(longTermDebtAvg)
# 	if processedData == 0 or processedData == None:
# 		processedData = 1
# 	ROCE = (Decimal(EBIT) / Decimal(processedData)) * 100
# 	return ROCE

#
def debtToEquityFormula(totalDebtCY=0, totalDebtPY=0, totalEquityCY=0, totalEquityPY=0):
    if totalEquityCY == None:
        totalEquityCY = 0.00
    if totalEquityPY == None:
        totalEquityPY = 0.00
    if totalDebtCY == None:
        totalDebtCY = 0.00
    if totalDebtPY == None:
        totalDebtPY = 0.00
    totalEquityPlus = Decimal(totalEquityCY) + Decimal(totalEquityPY)
    totalEquityAvg = Decimal(totalEquityPlus) / Decimal(2)
    totalDebtPlus = Decimal(totalDebtCY) + Decimal(totalDebtPY)
    totalDebtAvg = Decimal(totalDebtPlus) / Decimal(2)
    if totalEquityAvg == 0 or totalEquityAvg == None:
        totalEquityAvg = 1
    debtToEquity = Decimal(totalDebtAvg) / Decimal(totalEquityAvg)
    return debtToEquity


#
class roeSelfObj:
    def __init__(self, year=None, value=None):
        self.year = year
        self.value = value


#
def ROEgrowthCalculator(stock):
    profitAndLossObjs = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('-year')
    totalYearsData = []
    roeList = []
    ROEDict = {}
    netIncomeCY = None
    totalEquityCY = None
    totalEquityPY = None
    for item in profitAndLossObjs:
        totalYearsData.append(item.year)
    if (len(totalYearsData) > 1):
        forloopCounter = 0
        for i, j in enumerate(totalYearsData[:-1]):
            forloopCounter += 1
            firstYear = j
            prevYear = totalYearsData[i + 1]
            CYProfLoss = stockProfitAndLoss.objects.get(stockProfileName=stock, year=firstYear)
            try:
                CYBalanceSheet = stockBalanceSheet.objects.get(stockProfileName=stock, year=firstYear)
            except:
                CYBalanceSheet = 0
            try:
                PYBalanceSheet = stockBalanceSheet.objects.get(stockProfileName=stock, year=prevYear)
            except:
                PYBalanceSheet = 0
            if CYProfLoss.netIncome:
                netIncomeCY = Decimal(CYProfLoss.netIncome)
            if CYBalanceSheet:
                if CYBalanceSheet.totalEquity:
                    totalEquityCY = CYBalanceSheet.totalEquity
            if PYBalanceSheet:
                if PYBalanceSheet.totalEquity:
                    totalEquityPY = PYBalanceSheet.totalEquity
            calculatedROE = ROEFormula(netIncomeCY, totalEquityCY, totalEquityPY)
            ROEDict[firstYear] = calculatedROE
            roeObj = roeSelfObj(year=firstYear, value=calculatedROE)
            roeList.append(roeObj)
        ROEDictNew = calculateForListGrowthNewRoe(roeList, 'roe')

        # print('---------------------')
        # print(f'ROE List: {roeList}')
        # print(f'ROE Produced Dict: {ROEDictNew}')
        # print('///---------------------///')
        # ROEDict = calculateProgrammedGrowth(ROEDict)
        return ROEDictNew
    else:
        return False


#
def currentStockPEPBView(currentStock):
    stock = currentStock
    currentStockPrice = localOrScreenerPriceView(stock)
    try:
        stockProfitAndLossInst = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
        basicEps = stockProfitAndLossInst.basicEPS
        dilutedEps = stockProfitAndLossInst.dilutedEPS
    except:
        basicEps = 1
        dilutedEps = 1

    eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
    PEvalue = round((return_val_or_0(currentStockPrice) / return_val_or_1(eps)), 2)

    try:
        bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
        bookValYear = bookValues.year
        totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=bookValYear)
        bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
    except:
        bookValues = bookValueCal = None
    if bookValues:
        bookVal = bookValueCal
    else:
        bookVal = 1

    PBvalue = round((return_val_or_0(currentStockPrice) / return_val_or_1(bookVal)), 2)
    return PEvalue, PBvalue


#
def currentStockPEPBBankNBFCView(currentStock):
    stock = currentStock
    currentStockPrice = localOrScreenerPriceView(stock)
    try:
        stockProfitAndLossInst = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
        basicEps = stockProfitAndLossInst.basicEPS
        dilutedEps = stockProfitAndLossInst.dilutedEPS
    except:
        basicEps = 1
        dilutedEps = 1

    eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
    PEvalue = round((return_val_or_0(currentStockPrice) / return_val_or_1(eps)), 2)

    try:
        bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
        bookValYear = bookValues.year
        totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=bookValYear)
        bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
    except:
        bookValues = bookValueCal = None
    if bookValues:
        bookVal = bookValueCal
    else:
        bookVal = 1

    PBvalue = round((return_val_or_0(currentStockPrice) / return_val_or_1(bookVal)), 2)
    return PEvalue, PBvalue


#
def peersView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)

    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
    if renderBankNBFCsTemplates:
        return peersForBankNBFCView(request, slug)
    netProfitMarginCY = revenueCY = 0.00
    allStockList = stockBasicDetail.objects.all()
    yearCY = onlyRevenue = ebitda = None
    revenuePeersCompanyList = peersCompanyLinking.objects.filter(stockProfileName=stock)
    totalInvPY = totalInvCY = totalRevCY = totalIntangiblesCY = totalIntangiblesPY = totalAssetCY = totalAssetPY = netIncomeCY = totalEquityCY = totalEquityPY = EBITCY = longTermDebtCY = longTermDebtPY = 0.00
    totalAssetTurnoverRatioCY = totalFixedAssetTurnoverRatioCY = ROECY = ROCECY = debtToEquity = 0.00
    totalLngDebtCY = currPortLngTermDebtCY = currPortionLeasesCY = lngTermPortionOfLeasesCY = 0.0
    totalLngDebtPY = currPortLngTermDebtPY = currPortionLeasesPY = lngTermPortionOfLeasesPY = 0.0
    totalNonCurrentLiabilityCY = totalNonCurrentLiabilityPY = 0.0

    # revenueGraphData = {}
    screenerDict = {}
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None
    try:
        latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestProfitAndLoss = 0.00
    try:
        latestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestBalanceSheet = 0.00
    try:
        secondLatestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('-year')[1:2]
    except:
        secondLatestBalanceSheet = 0.00
    cashAndShortTermBalSheet = minorityInterestVal = totalCalculatedLnDebtCY = 0
    if latestBalanceSheet:
        cashAndShortTermBalSheet = latestBalanceSheet.cashAndShortTermInvestments
        minorityInterestVal = latestBalanceSheet.minorityInterest
        for item in secondLatestBalanceSheet:
            if item:
                if latestProfitAndLoss != 0.00:
                    if latestProfitAndLoss.revenue:
                        yearCY = latestProfitAndLoss.year
                        if latestProfitAndLoss.revenue:
                            totalRevCY = Decimal(latestProfitAndLoss.revenue)
                        if latestBalanceSheet.totalInventory:
                            totalInvCY = Decimal(latestBalanceSheet.totalInventory)
                        if item.totalInventory:
                            totalInvPY = Decimal(item.totalInventory)
                        if latestBalanceSheet.otherIntangibleAssests:
                            totalIntangiblesCY = Decimal(latestBalanceSheet.otherIntangibleAssests)
                        if item.otherIntangibleAssests:
                            totalIntangiblesPY = Decimal(item.otherIntangibleAssests)
                        if latestBalanceSheet.totalAssets:
                            totalAssetCY = Decimal(latestBalanceSheet.totalAssets)
                        if item.totalAssets:
                            totalAssetPY = Decimal(item.totalAssets)
                        if latestProfitAndLoss.netIncome:
                            netIncomeCY = Decimal(latestProfitAndLoss.netIncome)
                        if latestBalanceSheet.totalEquity:
                            totalEquityCY = Decimal(latestBalanceSheet.totalEquity)
                        if item.totalEquity:
                            totalEquityPY = Decimal(item.totalEquity)
                        if latestProfitAndLoss.pbit:
                            EBITCY = Decimal(latestProfitAndLoss.pbit)
                        if latestBalanceSheet.totalLongTermDebt:
                            totalLngDebtCY = Decimal(latestBalanceSheet.totalLongTermDebt)
                        if item.totalLongTermDebt:
                            totalLngDebtPY = Decimal(item.totalLongTermDebt)
                        if latestBalanceSheet.currentPortionOfLongTermDebt:
                            currPortLngTermDebtCY = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
                        if item.currentPortionOfLongTermDebt:
                            currPortLngTermDebtPY = Decimal(item.currentPortionOfLongTermDebt)
                        if latestBalanceSheet.currentPortionOfLeases:
                            currPortionLeasesCY = Decimal(latestBalanceSheet.currentPortionOfLeases)
                        if item.currentPortionOfLeases:
                            currPortionLeasesPY = Decimal(item.currentPortionOfLeases)
                        if latestBalanceSheet.longTermPortionOfLeases:
                            lngTermPortionOfLeasesCY = Decimal(latestBalanceSheet.longTermPortionOfLeases)
                        if item.longTermPortionOfLeases:
                            lngTermPortionOfLeasesPY = Decimal(item.longTermPortionOfLeases)
                        if latestBalanceSheet.nonCurrentLiabilities:
                            totalNonCurrentLiabilityCY = Decimal(latestBalanceSheet.nonCurrentLiabilities)
                        if item.nonCurrentLiabilities:
                            totalNonCurrentLiabilityPY = Decimal(item.nonCurrentLiabilities)

                        totalCalculatedLnDebtCY = Decimal(totalLngDebtCY) + Decimal(currPortLngTermDebtCY) + Decimal(
                            currPortionLeasesCY) + Decimal(lngTermPortionOfLeasesCY)
                        totalCalculatedLnDebtPY = Decimal(totalLngDebtPY) + Decimal(currPortLngTermDebtPY) + Decimal(
                            currPortionLeasesPY) + Decimal(lngTermPortionOfLeasesPY)

                        totalAssetTurnoverRatioCY = round(
                            totalAssetTurnoverRatioFormula(totalRevCY, totalAssetCY, totalAssetPY), 2)
                        totalFixedAssetTurnoverRatioCY = round(
                            totalFixedAssetTurnoverRatioFormula(totalRevCY, totalInvCY, totalInvPY), 2)
                        ROECY = round(ROEFormula(netIncomeCY, totalEquityCY, totalEquityPY), 2)
                        ROCECY = round(ROCEFormula(EBITCY, totalEquityCY, totalEquityPY, totalNonCurrentLiabilityCY,
                                                   totalNonCurrentLiabilityPY), 2)
                        debtToEquity = round(
                            debtToEquityFormula(totalCalculatedLnDebtCY, totalCalculatedLnDebtPY, totalEquityCY,
                                                totalEquityPY), 2)
    if latestProfitAndLoss:
        if latestProfitAndLoss.totalRevenue:
            revenueCY = round(latestProfitAndLoss.totalRevenue, 2)
        if latestProfitAndLoss.revenue:
            onlyRevenue = round(latestProfitAndLoss.revenue, 2)
        if latestProfitAndLoss.ebidta:
            ebitda = round(latestProfitAndLoss.ebidta, 2)
        # changes in NPM - Peers starts (Formula changed - It should be revenue of operations insted of Total Revenue )
        netProfitMarginCY = round(netProfitMarginFormula(latestProfitAndLoss.netIncome, latestProfitAndLoss.revenue), 2)
    # changes in NPM - Peers ends

    peRatioCS, pbRatioCS = currentStockPEPBView(stock)
    try:
        essentialInst = stockEssentials.objects.get(stockProfileName=stock)
    except:
        essentialInst = None
    marketCapCS = marketCapView(stock)
    if onlyRevenue == 0 or onlyRevenue == None:
        onlyRevenue = 1

    marketCapBySales = return_val_or_0(marketCapCS) / return_val_or_1(onlyRevenue)

    if essentialInst:
        enterpriseValueInst = essentialInst.enterpriseValue
        balanceWithRBIVal = essentialInst.balance_with_RBI
        preferenceEquityVal = essentialInst.preference_equity
    else:
        enterpriseValueInst = 0
        balanceWithRBIVal = preferenceEquityVal = 0
    if ebitda == 0:
        ebitda = 1

    try:
        if stock.stockProfileNameFFU.financialNumbers == 'L':
            marketCapCS = numberConversion(marketCapCS, currentSystem='Cr',
                                           convertTo=stock.stockProfileNameFFU.financialNumbers)
    except:
        pass

    # print(enterpriseVal)

    enterpriseVal = return_val_or_0(marketCapCS) - (
            return_val_or_0(cashAndShortTermBalSheet) - return_val_or_0(balanceWithRBIVal)) + return_val_or_0(
        totalCalculatedLnDebtCY) + return_val_or_0(preferenceEquityVal) + return_val_or_0(minorityInterestVal)

    # numberConversion
    # enterpriseVal = numberConversion(enterpriseVal, currentSystem='L', convertTo=stock.stockProfileNameFFU.financialNumbers)
    evByEbitda = round(return_val_or_0(enterpriseVal) / return_val_or_1(ebitda), 2)
    # conversion

    try:
        if stock.stockProfileNameFFU.financialNumbers == 'L':
            marketCapBySales = numberConversion(marketCapBySales, currentSystem='Cr',
                                                convertTo=stock.stockProfileNameFFU.financialNumbers)
    except:
        pass

    marketCapBySales = round(marketCapBySales, 2)

    screenerDict[stock] = {
        'id': stock.id,
        'type': 'current',
        'revenue': revenueCY,
        'netProfitMargin': netProfitMarginCY,
        'assetTurnoverRation': totalAssetTurnoverRatioCY,
        'totalFixedAssetTurnoverRatio': totalFixedAssetTurnoverRatioCY,
        'ROE': ROECY,
        'ROCE': ROCECY,
        'deptToEquity': debtToEquity,
        'peGraph': peRatioCS,
        'pbGraph': pbRatioCS,
        'marketCap': round(return_val_or_0(marketCapCS), 2),
        'marketCapBySales': marketCapBySales,
        'evByEbitda': evByEbitda,
    }

    fetchForYear = int(currentYear) - 1
    if latestProfitAndLoss:
        if latestProfitAndLoss.year:
            fetchForYear = latestProfitAndLoss.year
    for company in revenuePeersCompanyList:
        if company.stockStatus == 'Listed' and company.screenerLink:
            screenerDict[company] = crawlScreenerView(company, fetchForYear=fetchForYear)
        else:
            yearlyData = peerLinkingYearlyData.objects.filter(screenerCompany=company)
            try:
                stockYearData = yearlyData.get(year=fetchForYear)
                screenerDict[company] = {
                    'id': company.pk,
                    'type': company.stockStatus,
                    'fetchedUrl': '',
                    'revenue': stockYearData.revenue,
                    'netProfitMargin': stockYearData.netProfitMargin,
                    'assetTurnoverRation': stockYearData.assetTurnoverRation,
                    'ROE': stockYearData.ROE,
                    'ROCE': stockYearData.ROCE,
                    'deptToEquity': stockYearData.deptToEquity,
                    'peGraph': stockYearData.peRatio,
                    'pbGraph': stockYearData.pbRatio,
                    'marketCap': stockYearData.marketCap,
                    'marketCapBySales': stockYearData.marketCapBySales,
                    'enterpriseVal': stockYearData.enterpriseValue,
                    'evByEbitda': stockYearData.evByEbitda,
                    'cashAndShortTermEquivalents': stockYearData.cashAndShortTermCashEquivalents,
                    'PreferenceEquity': stockYearData.PreferenceEquity,
                    'totalMinorityInterest': stockYearData.totalMinorityInterest,
                    'longTermMarketableSecurities': stockYearData.longTermMarketableSecurities,
                    'yearNotAvailable': '',
                    'yearlyData': yearlyData,
                }
            except:
                screenerDict[company] = {
                    'id': company.pk,
                    'type': company.stockStatus,
                    'fetchedUrl': '',
                    'revenue': 0,
                    'netProfitMargin': 0,
                    'assetTurnoverRation': 0,
                    'ROE': 0,
                    'ROCE': 0,
                    'deptToEquity': 0,
                    'peGraph': 0,
                    'pbGraph': 0,
                    'marketCap': 0,
                    'marketCapBySales': 0,
                    'enterpriseVal': 0,
                    'evByEbitda': 0,
                    'cashAndShortTermEquivalents': 0,
                    'PreferenceEquity': 0,
                    'totalMinorityInterest': 0,
                    'longTermMarketableSecurities': 0,
                    'yearNotAvailable': '',
                    'yearlyData': yearlyData,
                }
    try:
        stockPeersDescInst = stockPeers.objects.get(stockProfileName=stock)
    except:
        stockPeersDescInst = None
    peersCompanyDesc = stockPeersForm(instance=stockPeersDescInst)
    peersCompanyLinkingCreate = peersCompanyLinkingForm()
    despositoryOptions, saleType = rightSideMenuObjs()
    if revenueCY == 0.00 and netProfitMarginCY == 0.00 and \
            totalAssetTurnoverRatioCY == 0.00 and totalFixedAssetTurnoverRatioCY == 0.00 and \
            ROECY == 0.00 and ROCECY == 0.00 and debtToEquity == 0.00 and peRatioCS and \
            pbRatioCS == 0.00 and marketCapCS == 0.00 and marketCapBySales == 0.00 and evByEbitda == 0.00:
        visiblity = False
    else:
        visiblity = True
    createpeerLinkingYearlyDataForm = peerLinkingYearlyDataForm()
    try:
        newsVideosheadpeers = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadpeers = []

    try:
        typeofcompanyInstpeers = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstpeers = None

    context = {
        'stock': stock,
        'allStockList': allStockList,
        'newsVideosheadpeers': newsVideosheadpeers,
        'typeofcompanyInstpeers': typeofcompanyInstpeers,
        'peersCompanyDesc': peersCompanyDesc,
        'stockPeersDescInst': stockPeersDescInst,
        'stockAdmInst': stockAdmInst,
        'peersCompanyLinkingCreate': peersCompanyLinkingCreate,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'visible': visiblity,
        'screenerDict': screenerDict,
        'year': yearCY,
        'createpeerLinkingYearlyDataForm': createpeerLinkingYearlyDataForm,
    }
    return render(request, 'UI/peers.html', context)


#
def peersForBankNBFCView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    yearCY = totalRevenueCY = netInterestIncomeCY = None
    revenuePeersCompanyList = peersCompanyLinkingForBankNBFC.objects.filter(stockProfileName=stock)
    currentPrice = localOrScreenerPriceView(stock)
    screenerDict = {}
    graphVisiblity = {}
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None
    try:
        latestProfitAndLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestProfitAndLoss = None
    try:
        latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestBalanceSheet = 0.00
    try:
        secondLatestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')[
                                   1:2]
    except:
        secondLatestBalanceSheet = 0.00
    # latest Profit and Loss
    netInterestIncomeCY = totalRevenueCY = netProfitCY = netInterestIncomeCY = dilutedEPSCY = basicEPSCY = 0
    if latestProfitAndLoss:
        yearCY = latestProfitAndLoss.year
        if latestProfitAndLoss.netInterestIncome:
            netInterestIncomeCY = Decimal(latestProfitAndLoss.netInterestIncome)
            graphVisiblity['netInterestIncomeGraph'] = True
        else:
            graphVisiblity['netInterestIncomeGraph'] = False
        if latestProfitAndLoss.totalRevenue:
            totalRevenueCY = Decimal(latestProfitAndLoss.totalRevenue)
            graphVisiblity['revenueGraph'] = True
        else:
            graphVisiblity['revenueGraph'] = False
        if latestProfitAndLoss.netIncome:
            netProfitCY = Decimal(latestProfitAndLoss.netIncome)
        if latestProfitAndLoss.basicEPS:
            basicEPSCY = Decimal(latestProfitAndLoss.basicEPS)
        if latestProfitAndLoss.dilutedEPS:
            dilutedEPSCY = Decimal(latestProfitAndLoss.dilutedEPS)
    # latest Balance Sheet
    totalAssetCY = totalEquityCY = longTermBorrowingsCY = shortTermBorrowingsCY = 0
    leaseLiabilityCY = currentPortionOfLongTermDebtCY = tangibleBookValueCY = 0
    totalCommonSharesOutstandingCY = tier1CapitalRatioCY = tier2CapitalRatioCY = aumCY = 0
    if latestBalanceSheet:
        if latestBalanceSheet.totalAssets:
            totalAssetCY = latestBalanceSheet.totalAssets
        if latestBalanceSheet.totalEquity:
            totalEquityCY = latestBalanceSheet.totalEquity
        if latestBalanceSheet.longTermBorrowings:
            longTermBorrowingsCY = latestBalanceSheet.longTermBorrowings
        if latestBalanceSheet.shortTermBorrowings:
            shortTermBorrowingsCY = latestBalanceSheet.shortTermBorrowings
        if latestBalanceSheet.leaseLiability:
            leaseLiabilityCY = latestBalanceSheet.leaseLiability
        if latestBalanceSheet.currentPortionOfLongTermDebt:
            currentPortionOfLongTermDebtCY = latestBalanceSheet.currentPortionOfLongTermDebt
        if latestBalanceSheet.tangibleBookValue:
            tangibleBookValueCY = latestBalanceSheet.tangibleBookValue
        if latestBalanceSheet.totalCommonSharesOutstanding:
            totalCommonSharesOutstandingCY = latestBalanceSheet.totalCommonSharesOutstanding
        if latestBalanceSheet.tier1CapitalRatio:
            tier1CapitalRatioCY = latestBalanceSheet.tier1CapitalRatio
            graphVisiblity['tier1Graph'] = True
        else:
            graphVisiblity['tier1Graph'] = False
        if latestBalanceSheet.tier2CapitalRatio:
            tier2CapitalRatioCY = latestBalanceSheet.tier2CapitalRatio
            graphVisiblity['tier2Graph'] = True
        else:
            graphVisiblity['tier2Graph'] = False
        if latestBalanceSheet.aum:
            aumCY = latestBalanceSheet.aum
            graphVisiblity['totalAMUGraph'] = True
        else:
            graphVisiblity['totalAMUGraph'] = False
    # Second latest Balance Sheet
    totalAssetsPY = totalEquityPY = longTermBorrowingsPY = shortTermBorrowingsPY = leaseLiabilityPY = currentPortionOfLongTermDebtPY = 0
    for item in secondLatestBalanceSheet:
        if item:
            if item.totalAssets:
                totalAssetsPY = item.totalAssets
            if item.totalEquity:
                totalEquityPY = item.totalEquity
            if item.longTermBorrowings:
                longTermBorrowingsPY = item.longTermBorrowings
            if item.shortTermBorrowings:
                shortTermBorrowingsPY = item.shortTermBorrowings
            if item.leaseLiability:
                leaseLiabilityPY = item.leaseLiability
            if item.currentPortionOfLongTermDebt:
                currentPortionOfLongTermDebtPY = item.currentPortionOfLongTermDebt
    # Calculating Averages
    avgTotalAsset = avgTotalEquity = avgOfSumNumeratorDE = None
    # if totalAssetCY and totalAssetsPY:
    avgTotalAsset = (return_val_or_0(totalAssetCY) + return_val_or_0(totalAssetsPY)) / 2
    # if totalEquityCY and totalEquityPY:
    avgTotalEquity = (return_val_or_0(totalEquityCY) + return_val_or_0(totalEquityPY)) / 2
    sumForDENumeratorCY = sumForDENumeratorPY = None
    # if longTermBorrowingsCY and shortTermBorrowingsCY and leaseLiabilityCY and currentPortionOfLongTermDebtCY:
    sumForDENumeratorCY = return_val_or_0(longTermBorrowingsCY) + return_val_or_0(
        shortTermBorrowingsCY) + return_val_or_0(leaseLiabilityCY) + return_val_or_0(currentPortionOfLongTermDebtCY)
    # if longTermBorrowingsPY and shortTermBorrowingsPY and leaseLiabilityPY and currentPortionOfLongTermDebtPY:
    sumForDENumeratorPY = return_val_or_0(longTermBorrowingsPY) + return_val_or_0(
        shortTermBorrowingsPY) + return_val_or_0(leaseLiabilityPY) + return_val_or_0(currentPortionOfLongTermDebtPY)
    # if sumForDENumeratorCY and sumForDENumeratorPY:
    avgOfSumNumeratorDE = (sumForDENumeratorCY + sumForDENumeratorPY) / 2
    # formulas and calculations
    # if netProfitCY and avgTotalAsset:
    roa = return_val_or_0(netProfitCY) / return_val_or_1(avgTotalAsset)
    if roa and roa != 0:
        graphVisiblity['roaGraph'] = True
    else:
        graphVisiblity['roaGraph'] = False
    # else:
    # 	roa = 0
    # if netProfitCY and netInterestIncomeCY:
    netProfitMarginPercentage = (return_val_or_0(netProfitCY) / return_val_or_1(netInterestIncomeCY)) * 100
    if netProfitMarginPercentage and netProfitMarginPercentage != 0:
        graphVisiblity['netProfitMarginPercentageGraph'] = True
    else:
        graphVisiblity['netProfitMarginPercentageGraph'] = False
    # else:
    # 	netProfitMarginPercentage = 0
    # if netInterestIncomeCY and avgTotalAsset:
    assetTurnOverRatio = return_val_or_0(netInterestIncomeCY) / return_val_or_1(avgTotalAsset)
    if assetTurnOverRatio and assetTurnOverRatio != 0:
        graphVisiblity['assetTurnOverRatioGraph'] = True
    else:
        graphVisiblity['assetTurnOverRatioGraph'] = False
    # else:
    # 	assetTurnOverRatio = 0
    # if netProfitCY and avgTotalEquity:
    roeGraph = False
    roe = return_val_or_0(netProfitCY) / return_val_or_1(avgTotalEquity)
    if roe and roe != 0:
        graphVisiblity['roeGraph'] = True
    else:
        graphVisiblity['roeGraph'] = False
    # else:
    # roe = 0
    # eps = check_eps_basic_or_diluted(basicEPSCY, dilutedEPSCY)
    # if currentPrice and eps:
    # 	priceToEarning = currentPrice / eps
    # else:
    # 	priceToEarning = 0
    priceToEarning, priceToBookVal = currentStockPEPBBankNBFCView(stock)
    if priceToEarning and priceToEarning != 0:
        graphVisiblity['priceToEarningGraph'] = True
    else:
        graphVisiblity['priceToEarningGraph'] = False
    if priceToBookVal and priceToBookVal != 0:
        graphVisiblity['priceToBookValGraph'] = True
    else:
        graphVisiblity['priceToBookValGraph'] = False

    # try:
    # 	bookValueObj = bookValueData.objects.get(stockProfileName=stock,year=yearCY)
    # 	bookValueCY = bookValueObj.bookValue
    # except:
    # 	bookValueCY = 0
    # if currentPrice and bookValueCY:
    # 	if bookValueCY == 0:
    # 		bookValueCY = 1
    # 	priceToBookVal = currentPrice / bookValueCY
    # else:
    # 	priceToBookVal = 0
    # if netInterestIncomeCY and avgTotalAsset:
    nim = return_val_or_0(netInterestIncomeCY) / return_val_or_1(avgTotalAsset)
    if nim and nim != 0:
        graphVisiblity['nimGraph'] = True
    else:
        graphVisiblity['nimGraph'] = False
    # else:
    # 	nim = 0
    # if avgTotalEquity and avgOfSumNumeratorDE:
    debtToEquityRatioGraph = False
    debtToEquityRatio = return_val_or_0(avgOfSumNumeratorDE) / return_val_or_1(avgTotalEquity)
    if debtToEquityRatio and debtToEquityRatio != 0:
        graphVisiblity['debtToEquityRatioGraph'] = True
    else:
        graphVisiblity['debtToEquityRatioGraph'] = False
    # else:
    # 	debtToEquityRatio = 0

    # Coming from Key Ratios
    try:
        rorwaGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock,
                                                                    graphFor='Return on Risk Weighted Assets(RORWA)')
        rorwaInstCY = industrySpecificGraphsValues.objects.get(valuesFor=rorwaGraphFromKeyRatio, year=yearCY)
        RORWAVal = rorwaInstCY.value
        graphVisiblity['RORWAGraph'] = True
    except:
        RORWAVal = 0
        graphVisiblity['RORWAGraph'] = False
    try:
        netNPAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='Net NPA')
        netNPAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=netNPAGraphFromKeyRatio, year=yearCY)
        netNPAVal = netNPAInstCY.value
        graphVisiblity['netNPAGraph'] = True
    except:
        netNPAVal = 0
        graphVisiblity['netNPAGraph'] = False
    try:
        CASAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='CASA')
        CASAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=CASAGraphFromKeyRatio, year=yearCY)
        CASAVal = CASAInstCY.value
        graphVisiblity['casaGraph'] = True
    except:
        CASAVal = 0
        graphVisiblity['casaGraph'] = False
    try:
        grossNPAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='Gross NPA')
        grossNPAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=grossNPAGraphFromKeyRatio, year=yearCY)
        grossNPAVal = grossNPAInstCY.value
        graphVisiblity['grossNPAValGraph'] = True
    except:
        grossNPAVal = 0
        graphVisiblity['grossNPAValGraph'] = False
    try:
        CARGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock,
                                                                  graphFor='Capital Adequacy Ratio(CAR)')
        CARInstCY = industrySpecificGraphsValues.objects.get(valuesFor=CARGraphFromKeyRatio, year=yearCY)
        carVal = CARInstCY.value
        graphVisiblity['carGraph'] = True
    except:
        carVal = 0
        graphVisiblity['carGraph'] = False
    # P/TB Calculation
    # if currentPrice and tangibleBookValueCY and totalCommonSharesOutstandingCY:
    # 	if totalCommonSharesOutstandingCY == 0:
    # 		totalCommonSharesOutstandingCY = 1
    pByTB = return_val_or_0(currentPrice) / return_val_or_1(
        (return_val_or_0(tangibleBookValueCY) * 10000000) / return_val_or_1(totalCommonSharesOutstandingCY))
    if pByTB and pByTB != 0:
        graphVisiblity['pByTBGraph'] = True
    else:
        graphVisiblity['pByTBGraph'] = False
    # else:
    # 	pByTB = 0
    marketCapCS = marketCapView(stock)
    try:
        if stock.stockProfileNameFFU.financialNumbers == 'L':
            marketCapCS = numberConversion(marketCapCS, currentSystem='Cr',
                                           convertTo=stock.stockProfileNameFFU.financialNumbers)
    except:
        pass
    # print('---------------------------------------------------------------------Jhalak new TESTSTING STARTSSSSSSSS---------------------------------------------------------------------')
    # print(marketCapCS)
    # print('---------------------------------------------------------------------Jhalak new TESTSTING ENDDDDDDDSSSS---------------------------------------------------------------------')
    screenerDict[stock] = {
        'id': stock.id,
        'type': 'current',
        'revenue': round(return_val_or_0(totalRevenueCY), 2),
        'netInterestIncome': round(return_val_or_0(netInterestIncomeCY), 2),

        'marketCap': round(return_val_or_0(marketCapCS), 2),

        'roa': round((roa * 100), 2),
        'netProfitMarginPercentage': round(netProfitMarginPercentage, 2),
        'assetTurnOverRatio': round(assetTurnOverRatio, 2),
        'roe': round((roe * 100), 2),
        'car': round(carVal, 2),
        'netNPA': round(netNPAVal, 2),
        'grossNPA': round(grossNPAVal, 2),
        'stockPE': round(priceToEarning, 2),
        'stockPB': round(priceToBookVal, 2),
        'nim': round((nim * 100), 2),
        'CASA': round(CASAVal, 2),
        'debtToEquityRatio': round(debtToEquityRatio, 2),
        'pByTB': round(pByTB, 2),
        'tier1': round(tier1CapitalRatioCY, 2),
        'tier2': round(tier2CapitalRatioCY, 2),
        'totalAMU': round(aumCY, 2),
        'RORWA': round(RORWAVal, 2),
    }
    fetchForYear = int(currentYear) - 1
    if latestProfitAndLoss:
        if latestProfitAndLoss.year:
            fetchForYear = latestProfitAndLoss.year
    for company in revenuePeersCompanyList:
        if company.stockStatus == 'Listed' and company.screenerLink:
            someVal = crawlScreenerForBankNBFCView(company, fetchForYear=fetchForYear)
            screenerDict[company] = someVal
        else:
            unlistedYearlyData = peerLinkingYearlyDataForBankNBFC.objects.filter(screenerCompany=company)
            try:
                companyYearlyInst = unlistedYearlyData.get(year=fetchForYear)
                manualCAR = companyYearlyInst.CAR
                manualMarketCap = companyYearlyInst.marketCap
                manualnetNPA = companyYearlyInst.netNPA
                manualgrossNPA = companyYearlyInst.grossNPA
                manualCASA = companyYearlyInst.CASA
                manualtier1CapitalRatio = companyYearlyInst.tier1CapitalRatio
                manualtier2CapitalRatio = companyYearlyInst.tier2CapitalRatio
                manualtotalAMU = companyYearlyInst.totalAMU
                manualRORWA = companyYearlyInst.RORWA
                manualnumberOfShares = companyYearlyInst.numberOfShares
                manualintangibleAssests = companyYearlyInst.intangibleAssests
                manualnetInterestIncome = companyYearlyInst.netInterestIncome
                manualrevenue = companyYearlyInst.revenue
                manualroa = companyYearlyInst.roa
                manualnetProfitMargin = companyYearlyInst.netProfitMargin
                manualassetTurnOverRatio = companyYearlyInst.assetTurnOverRatio
                manualROE = companyYearlyInst.ROE
                manualpeRatio = companyYearlyInst.peRatio
                manualpbRatio = companyYearlyInst.pbRatio
                manualNIM = companyYearlyInst.NIM
                manualDERatio = companyYearlyInst.DERatio
                manualpriceByTangibleBookRatio = companyYearlyInst.priceByTangibleBookRatio
                if company.screenerLink:
                    manualScreenerLink = company.screenerLink
                else:
                    manualScreenerLink = None
            except:
                manualCAR = 0
                manualMarketCap = 0
                manualnetNPA = 0
                manualgrossNPA = 0
                manualCASA = 0
                manualtier1CapitalRatio = 0
                manualtier2CapitalRatio = 0
                manualtotalAMU = 0
                manualRORWA = 0
                manualnumberOfShares = 0
                manualintangibleAssests = 0
                manualnetInterestIncome = 0
                manualrevenue = 0
                manualroa = 0
                manualnetProfitMargin = 0
                manualassetTurnOverRatio = 0
                manualROE = 0
                manualpeRatio = 0
                manualpbRatio = 0
                manualNIM = 0
                manualDERatio = 0
                manualpriceByTangibleBookRatio = 0
                manualScreenerLink = None
            screenerDict[company] = {
                'id': company.id,
                'type': 'Unlisted',
                'car': manualCAR,
                'marketCap': manualMarketCap,
                'netNPA': manualnetNPA,
                'grossNPA': manualgrossNPA,
                'CASA': manualCASA,
                'tier1': manualtier1CapitalRatio,
                'tier2': manualtier2CapitalRatio,
                'totalAMU': manualtotalAMU,
                'RORWA': manualRORWA,
                'numberOfShares': manualnumberOfShares,
                'intangibleAssests': manualintangibleAssests,
                'netInterestIncome': manualnetInterestIncome,
                'revenue': manualrevenue,
                'roa': manualroa,
                'netProfitMarginPercentage': manualnetProfitMargin,
                'assetTurnOverRatio': manualassetTurnOverRatio,
                'roe': manualROE,
                'stockPE': manualpeRatio,
                'stockPB': manualpbRatio,
                'nim': manualNIM,
                'debtToEquityRatio': manualDERatio,
                'pByTB': manualpriceByTangibleBookRatio,
                'fetchedUrl': manualScreenerLink,
                'yearlyData': unlistedYearlyData,
            }

    # if latestProfitAndLoss:
    # 	if latestProfitAndLoss.year:
    # 		fetchForYear = latestProfitAndLoss.year
    # 	else:
    # 		fetchForYear = 2021
    # for company in revenuePeersCompanyList:
    # 	if company.screenerLink:
    # 		dictForScreenerData = crawlScreenerForBankNBFCView(company, fetchForYear= fetchForYear)
    # 		return HttpResponse(str(dictForScreenerData))
    # 		screenerDict[company] = dictForScreenerData
    try:
        stockPeersDescInst = stockPeers.objects.get(stockProfileName=stock)
    except:
        stockPeersDescInst = None
    peersCompanyDesc = stockPeersForm(instance=stockPeersDescInst)
    peersCompanyLinkingCreate = peersCompanyLinkingForBankNBFCForm()
    # despositoryOptions, saleType = rightSideMenuObjs()
    createpeerLinkingYearlyDataForm = peerLinkingYearlyDataForBankNBFCForm()

    try:
        stockPeersDescriptionForBankNBFCInst = stockPeersDescriptionForBankNBFC.objects.get(stockProfileName=stock)
    except:
        stockPeersDescriptionForBankNBFCInst = None
    stockPeersDescriptionForBankNBFCInstForm = stockPeersDescriptionForBankNBFCForm(
        instance=stockPeersDescriptionForBankNBFCInst)

    if totalRevenueCY == 0.00 and netInterestIncomeCY == 0.00 and \
            marketCapCS == 0.00 and netProfitMarginPercentage == 0.00 and \
            assetTurnOverRatio == 0.00 and roa == 0.00 and roe == 0.00 and carVal and \
            netNPAVal == 0.00 and grossNPA == 0.00 and priceToEarning == 0.00 and priceToBookVal == 0.00 and \
            nim == 0.00 and CASAVal == 0.00 and debtToEquityRatio == 0.00 and pByTB == 0.00 and \
            tier1CapitalRatioCY == 0.00 and aumCY == 0.00 and RORWAVal == 0.00:
        visiblity = False
    else:
        visiblity = True

    try:
        newsVideosheadpeersforbanknbfc = blogVideos.objects.filter(showinhead=True,
                                                                   relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadpeersforbanknbfc = []

    try:
        typeofcompanyInstpeersforbanknbfc = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstpeersforbanknbfc = None
    context = {
        'stock': stock,
        'peersCompanyDesc': peersCompanyDesc,
        'newsVideosheadpeersforbanknbfc': newsVideosheadpeersforbanknbfc,
        'typeofcompanyInstpeersforbanknbfc': typeofcompanyInstpeersforbanknbfc,
        'stockPeersDescInst': stockPeersDescInst,
        'stockAdmInst': stockAdmInst,
        'peersCompanyLinkingCreate': peersCompanyLinkingCreate,
        'screenerDict': screenerDict,
        'year': yearCY,
        'createpeerLinkingYearlyDataForm': createpeerLinkingYearlyDataForm,
        'stockPeersDescriptionForBankNBFCInst': stockPeersDescriptionForBankNBFCInst,
        'stockPeersDescriptionForBankNBFCInstForm': stockPeersDescriptionForBankNBFCInstForm,
        'graphVisiblity': graphVisiblity,
        'visible': visiblity,
    }
    return render(request, 'UI/peersForBankNBFC.html', context)


#
def stockBasicDetailView(request, id=None):
    dataID = request.POST.get('dataID')
    stockBasicDetailInstance = None
    redirectTo = 'stockApp:stockListURL'
    if dataID:
        stockBasicDetailInstance = get_object_or_404(stockBasicDetail, pk=dataID)
    else:
        stockBasicDetailInstance = None
    if request.method == 'POST':
        viewStockBasicDetail = stockBasicDetailForm(request.POST, request.FILES, instance=stockBasicDetailInstance)
        if viewStockBasicDetail.is_valid():
            cd = viewStockBasicDetail.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            viewStockBasicDetail.save_m2m()
            cd.refresh_from_db()
            messages.success(request, 'Stock Basic Detail sent For Verification')
        else:
            messages.error(request, 'Wrong Input Data, Please check An Error occurred')
    return redirect(redirectTo)


#
def currentRateOfbondYieldView(request, id=None):
    currentRateInst = None
    redirectTo = 'stockApp:stockListURL'
    if id:
        currentRateInst = get_object_or_404(currentRateOfbondYield, pk=id)
    if request.method == 'POST':
        currentRateForm = currentRateOfbondYieldForm(request.POST, instance=currentRateInst)
        if currentRateForm.is_valid():
            cd = currentRateForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Current Rate of Bond sent For Verification')
        else:
            messages.error(request, 'Wrong Input Data, Please check An Error occurred')
    return redirect(redirectTo)


def stockListHeadingsubmitView(request, id=None):
    currentRateInst = None
    redirectTo = 'stockApp:stockListURL'
    if id:
        currentRateInst = get_object_or_404(stockListHeading, pk=id)
    if request.method == 'POST':
        currentRateForm = stockListHeadingForm(request.POST, instance=currentRateInst)
        if currentRateForm.is_valid():
            cd = currentRateForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent For Verification')
        else:
            messages.error(request, 'Wrong Input Data, Please check An Error occurred')
    return redirect(redirectTo)

def pitchupperimagessubmitView(request, id=None):
	pitchupperimagesInst = None
	redirectTo = 'stockApp:stockListURL'
	relatedStockId = request.POST.get('stockprofile')

	try:
		stockInst = stockBasicDetail.objects.get(id=relatedStockId)
	except:
		stockInst = None
	print(stockInst)
	if id:
		pitchupperimagesInst = get_object_or_404(pitchupperimage, pk=id)
	if request.method == 'POST':
		pitchupperimageFormInst = pitchupperimageForm(request.POST, request.FILES, instance=pitchupperimagesInst)
		if pitchupperimageFormInst.is_valid():
			cd = pitchupperimageFormInst.save(commit=False)
			if request.user.is_authenticated:
				cd.stockProfileName = stockInst
				cd.analyst = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent For Verification')
		else:
			messages.error(request, 'Wrong Input Data, Please check An Error occurred')
	return redirect(redirectTo)

#

def stockSpecificView(request, id=None):
    stockSpecificInst = None
    redirectTo = 'stockApp:stockListURL'
    if id:
        stockSpecificInst = get_object_or_404(stockAppSpecific, pk=id)
    if request.method == 'POST':
        stockSpecificForm = stockAppSpecificForm(request.POST, instance=stockSpecificInst)
        if stockSpecificForm.is_valid():
            cd = stockSpecificForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Specific Details sent For Verification')
        else:
            messages.error(request, 'Wrong Input Data, Please check An Error occurred')
    return redirect(redirectTo)


#
def companyDescriptionView(request, id=None):
    stockBasicDetailInstance = None
    redirectTo = 'stockApp:stockListURL'
    if id:
        stockBasicDetailInstance = get_object_or_404(stockBasicDetail, pk=id)
    if request.method == 'POST':
        viewStockBasicDetail = stockDetailsAboutForm(request.POST, instance=stockBasicDetailInstance)
        if viewStockBasicDetail.is_valid():
            cd = viewStockBasicDetail.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Basic Detail sent For Verification')
        else:
            messages.error(request, viewStockBasicDetail.errors)
    return redirect(redirectTo)


#
def awardsDescriptionView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objInst = None
        else:
            objInst = get_object_or_404(stockDetails, stockProfileName=stockProfile)  # Change Model Name
        objForm = stockDetailsAwardForm(request.POST, instance=objInst)  # Change Form Name
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Award Description sent For Verification')  # Change Msg Accordingly
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def SSOTDescriptionView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objInst = None
        else:
            objInst = get_object_or_404(stockDetails, stockProfileName=stockProfile)  # Change Model Name
        objForm = stockDetailsSSOTForm(request.POST, instance=objInst)  # Change Form Name
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'SSTO Description sent For Verification')  # Change Msg Accordingly
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def companyDescriptionView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objInst = None
        else:
            objInst = get_object_or_404(stockDetails, stockProfileName=stockProfile)  # Change Model Name
        objForm = stockDetailsAboutForm(request.POST, instance=objInst)  # Change Form Name
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Company About sent For Verification')  # Change Msg Accordingly
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockEssentialsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objInst = None
        else:
            objInst = get_object_or_404(stockEssentials, stockProfileName=stockProfile)  # Change Model Name
        objForm = stockEssentialsForm(request.POST, instance=objInst)  # Change Form Name
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Essentials sent For Verification')  # Change Msg Accordingly
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockEssentialsBottomView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objInst = None
        else:
            objInst = get_object_or_404(stockEssentials, stockProfileName=stockProfile)  # Change Model Name
        objForm = stockEssentialsBottomForm(request.POST, instance=objInst)  # Change Form Name
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Essentials sent For Verification')  # Change Msg Accordingly
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def bookValueDataViews(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        if methodType == 'new':
            objInst = None
            if bookValueData.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
                messages.error(request, 'Values Already Present for Entered Year.')
                return redirect(redirectTo)
        else:
            instID = request.POST.get('dataID')
            objInst = get_object_or_404(bookValueData, pk=instID)
        objForm = bookValueDataForm(request.POST, instance=objInst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Book Value Annual Data sent For Verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 2 finacialCompanyUpdates

def financialCompanyUpdatesView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('title')
        if methodType == 'new':
            objlnst = None
            if financialCompanyUpdates.objects.filter(stockProfileName=stockProfile, title=enteredYear).exists():
                messages.error(request, 'Values Already Present for Entered Year.')
                return redirect(redirectTo)
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(financialCompanyUpdates, pk=pkID)
        objForm = financialCompanyUpdatesForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Financial Company Updates sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def leadGenerationView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        redirectTo = request.POST.get('requestFrom')
        objForm = leadGenerationDetailsForm(request.POST)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Team will get back to you sooner.')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 3 stockBalanceSheet

def stockBalanceSheetView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        if not stockBalanceSheet.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
            if methodType == 'new':
                objlnst = None
            else:
                pkID = request.POST.get('dataID')
                objlnst = get_object_or_404(stockBalanceSheet, pk=pkID)
            objForm = stockBalanceSheetForm(request.POST, instance=objlnst)
            if objForm.is_valid():
                cd = objForm.save(commit=False)
                cd.stockProfileName = stockInst
                if request.user.is_authenticated:
                    cd.analyst = request.user
                cd.save()
                cd.refresh_from_db()
                messages.success(request, 'Stock BalanceSheet sent for verification')
            else:
                messages.error(request, objForm.errors)
        else:
            messages.error(request, 'Values Already Present for Entered Year.')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def financialFigureUnitsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(financialFigureUnits, stockProfileName=stockProfile)
        objForm = financialFigureUnitsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Financial Figure Units Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 1     recommendationOptions

def recommendationOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(recommendationOptions, stockProfileName=stockProfile)
        objForm = recommendationOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Recommendation Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 2       stockInvestmentChecklist

def stockInvestmentChecklistView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockInvestmentChecklist, stockProfileName=stockProfile)
        objForm = stockInvestmentChecklistForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Investment Checklist sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 3  stockAdmin
def stockAdminView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockAdmin, stockProfileName=stockProfile)
        objForm = stockAdminForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Admin sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockAdminDMView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        adminRequest = request.GET.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockAdmin, stockProfileName=stockProfile)
        if adminRequest == 'snapshot':
            objForm = stockAdminSnapshotForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'keyratio':
            objForm = stockAdminKeyRatioForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'peers':
            objForm = stockAdminPeersForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'financialBalanceSheet':
            objForm = stockAdminFinancialBalanceSheetForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'financialProfitLoss':
            objForm = stockAdminFinancialProfitLossForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'financialCashFlow':
            objForm = stockAdminFinancialCashFlowForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'ownership':
            objForm = stockAdminOwnershipForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'news':
            objForm = stockAdminNewsForm(request.POST, request.FILES, instance=objlnst)
        elif adminRequest == 'events':
            objForm = stockAdminEventsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Admin sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockListDMView(request):
    if request.method == 'POST':
        try:
            objInst = stockListDM.objects.latest('id')
        except:
            objInst = None
        objForm = stockListDMForm(request.POST, request.FILES, instance=objInst)
        if objForm.is_valid():
            cd = objForm.save()
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'DM Details for Stock List Page sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect('stockApp:stockListURL')
    return HttpResponse('Invalid Entry')


# 4  stockIPO

def stockIPOView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockIPO, stockProfileName=stockProfile)
        objForm = stockIPOForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock IPO sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 5   stageOptions

def stageOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stageOptions, stockProfileName=stockProfile)
        objForm = stageOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stage Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 6  lookingForOptions

def lookingForOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(lookingForOptions, stockProfileName=stockProfile)
        objForm = lookingForOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'looking For Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 7    currencySymbolOptions

def currencySymbolOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(currencySymbolOptions, stockProfileName=stockProfile)
        objForm = currencySymbolOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'currency Symbol Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 8  stockFunding

def stockFundingView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockFunding, stockProfileName=stockProfile)
        objForm = stockFundingForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Funding sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 9    stockFundingRounds

def stockFundingRoundsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockFundingRounds, pk=pkID)
        objForm = stockFundingRoundsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Funding Rounds sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 10  stockDetails

def stockDetailsMergerAcquistionView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockDetails, stockProfileName=stockProfile)
        objForm = stockDetailsFormMergerAcquistion(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Description sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockDetailsSubsidiariesBusModelView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockDetails, stockProfileName=stockProfile)
        objForm = stockDetailsSubsidiariesBusModelForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Description sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockDetailsProductView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockDetails, stockProfileName=stockProfile)
        objForm = stockDetailsProductForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Description sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockDetailsAssestView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockDetails, stockProfileName=stockProfile)
        objForm = stockDetailsAssestForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Description sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockDetailsIndustyOverviewView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockDetails, stockProfileName=stockProfile)
        objForm = stockDetailsIndustryOverviewForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Description sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 11   stockRevenueBreakUp
def stockRevenueBreakUpView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredItem = request.POST.get('items')
        if methodType == 'new':
            objlnst = None
            if stockRevenueBreakUp.objects.filter(stockProfileName=stockProfile, items=enteredItem).exists():
                messages.error(request, 'Values Already Present for Entered Item.')
                return redirect(redirectTo)
        else:
            dataInst = request.POST.get('dataID')
            objlnst = get_object_or_404(stockRevenueBreakUp, pk=dataInst)
        objForm = stockRevenueBreakUpForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Revenue BreakUp sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 12 profitabilityOptions
def profitabilityOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(profitabilityOptions, stockProfileName=stockProfile)
        objForm = profitabilityOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'profitability Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 13   solvencyOptions

def solvencyOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(solvencyOptions, stockProfileName=stockProfile)
        objForm = solvencyOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'solvency Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 14   growthOptions

def growthOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(growthOptions, stockProfileName=stockProfile)
        objForm = growthOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'growth Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 15  valuationOptions

def valuationOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(valuationOptions, stockProfileName=stockProfile)
        objForm = valuationOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'valuation Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 16   businessTypeOptions

def businessTypeOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(businessTypeOptions, stockProfileName=stockProfile)
        objForm = businessTypeOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'business Type Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# 17 stockOwnership

def stockOwnershipView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockOwnership, stockProfileName=stockProfile)
        objForm = stockOwnershipForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Ownership sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def stockOwnershipPostCallView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockOwnership, stockProfileName=stockProfile)
        objForm = stockOwnershipForm(request.data, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({"msg":"stock Events CorpActions sent for verification", "status": True})
        else:
            return Response({"msg":"Error occured while saving the data. Please check the format !", 'status' : False})
        # return redirect(redirectTo)
    return Response({'msg':'Invalid Entry', 'status' : False})

# 18  stockOwnershipDirector

def stockOwnershipDirectorView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockOwnershipDirector, pk=pkID)
        objForm = stockOwnershipDirectorForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Ownership Director sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def stockOwnershipDirectorPostCallView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(stockOwnershipDirector, pk=pkID)
        objForm = stockOwnershipDirectorForm(request.data, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({"msg":"stock Events CorpActions sent for verification", "status": True})
        else:
            return Response({"msg":"Error occured while saving the data. Please check the format !", 'status' : False})
        # return redirect(redirectTo)
    return Response({'msg':'Invalid Entry', 'status' : False})

# 19  stockOwnershipInstitutional

def stockOwnershipInstitutionalView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockOwnershipInstitutional, pk=pkID)
        objForm = stockOwnershipInstitutionalForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Ownership Institutional sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def stockOwnershipInstitutionalPostCallView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(stockOwnershipInstitutional, pk=pkID)
        objForm = stockOwnershipInstitutionalForm(request.data, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({"msg":"stock Events CorpActions sent for verification", "status": True})
        else:
            return Response({"msg":"Error occured while saving the data. Please check the format !", 'status' : False})
    return Response({'msg':'Invalid Entry', 'status' : False})
# 20 stockEventsCorpActions

def stockEventsCorpActionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockEventsCorpActions, pk=pkID)
        objForm = stockEventsCorpActionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Events CorpActions sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['POST'])
def stockEventsCorpActionsApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(stockEventsCorpActions, pk=pkID)
        objForm = stockEventsCorpActionsForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({"success":"stock Events CorpActions sent for verification"})
        else:
            return Response({"success":objForm.errors})
        return redirect(redirectTo)
    return Response({'msg':'Invalid Entry'})


# 21  announcementTypeOptions

def announcementTypeOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(announcementTypeOptions, stockProfileName=stockProfile)
        objForm = announcementTypeOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'announcement Type Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#  22 stockEventsAnnouncements

def stockEventsAnnouncementsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockEventsAnnouncements, pk=pkID)
        objForm = stockEventsAnnouncementsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Events Announcements sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')



@api_view(['POST'])
def stockEventsAnnouncementsApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(stockEventsAnnouncements, pk=pkID)
        objForm = stockEventsAnnouncementsForm(request.data, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({"Success":"'stock Events Announcements sent for verification'"})
        else:
            return Response({"success":objForm.errors})
    return Response({'msg':'Invalid Entry'})


# 23 legalOrdersOptions

# def legalOrdersOptionsView(request):
#     if request.method == 'POST':
#         stockProfile = request.POST.get('stockProfile')
#         stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
#         methodType = request.POST.get('submitType')
#         redirectTo = request.POST.get('requestFrom')
#         if methodType == 'new':
#             objlnst = None
#         else:
#             objlnst = get_object_or_404(legalOrdersOptions, stockProfileName = stockProfile)
#         objForm = legalOrdersOptionsForm(request.POST, instance=objlnst)
#         if objForm.is_valid():
#             cd = objForm.save(commit=False)
#             cd.stockProfileName = stockInst
#             if request.user.is_authenticated:
#                 cd.analyst = request.user
#             cd.save()
#             cd.refresh_from_db()
#             messages.success(request, 'legal Orders Options sent for verification')
#         else:
#             messages.error(request, objForm.errors)
#         return redirect(redirectTo)
#     return HttpResponse('Invalid Entry')


# 24 stockEventsLegalOrders

def stockEventsLegalOrdersView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockEventsLegalOrders, pk=pkID)
        objForm = stockEventsLegalOrdersForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stockEvents Legal Orders sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['POST'])
def stockEventsLegalOrdersApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(stockEventsLegalOrders, pk=pkID)
        objForm = stockEventsLegalOrdersForm(request.data, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({"status":"stockEvents Legal Orders sent for verification"})
        else:
            return Response({"status":objForm.errors})
    return Response({'msg':'Invalid Entry'})



#
def stockProfitAndLossView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        if methodType == 'new':
            objlnst = None
            if stockProfitAndLoss.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
                messages.error(request, 'Values Already Present for Entered Year.')
                return redirect(redirectTo)
        else:
            objlnst = get_object_or_404(stockProfitAndLoss, stockProfileName=stockProfile)
        objForm = stockProfitAndLossForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Profit AndLoss sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# def welcomePopupView(request):
# 	try:
# 		popupInst = welcomeLoginPopup.objects.latest(-id)
# 	except:
# 		popupInst = None
# 	welcomeLoginPopupInstForm = welcomeLoginPopupForm(instance=popupInst)

# 	context = {
# 	'popupInst':popupInst,
# 	'welcomeLoginPopupInstForm':welcomeLoginPopupInstForm,
# 	}

# 	return render(request, 'tempTagHTMl/letsBegin.html')

# def stockProfitAndLossView(request):
# 	if request.method == 'POST':
# 		stockProfile = request.POST.get('stockProfile')
# 		stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
# 		methodType = request.POST.get('submitType')
# 		redirectTo = request.POST.get('requestFrom')
# 		enteredYear = request.POST.get('year')
# 		if not stockProfitAndLoss.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
# 			if methodType == 'new':
# 				objlnst = None
# 			else:
# 				objlnst = get_object_or_404(stockProfitAndLoss, stockProfileName=stockProfile)
# 			objForm = stockProfitAndLossForm(request.POST, instance=objlnst)
# 			if objForm.is_valid():
# 				cd = objForm.save(commit=False)
# 				cd.stockProfileName = stockInst
# 				if request.user.is_authenticated:
# 					cd.analyst = request.user
# 				cd.save()
# 				cd.refresh_from_db()
# 				messages.success(request, 'Stock Profit AndLoss sent for verification')
# 			else:
# 				messages.error(request, objForm.errors)
# 		else:
# 			messages.error(request, 'Values Already Present for Entered Year.')
# 		return redirect(redirectTo)
# 	return HttpResponse('Invalid Entry')


def stockCashFlowView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        if not stockCashFlow.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
            if methodType == 'new':
                objlnst = None
            else:
                objlnst = get_object_or_404(stockCashFlow, stockProfileName=stockProfile)
            objForm = stockCashFlowForm(request.POST, instance=objlnst)
            if objForm.is_valid():
                cd = objForm.save(commit=False)
                cd.stockProfileName = stockInst
                if request.user.is_authenticated:
                    cd.analyst = request.user
                cd.save()
                cd.refresh_from_db()
                messages.success(request, 'Stock Cash Flow sent for verification')
            else:
                messages.error(request, objForm.errors)
        else:
            messages.error(request, 'Values Already Present for Entered Year.')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# old views

def stockTransferDepositoryOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockTransferDepositoryOptions, stockProfileName=stockProfile)
        objForm = stockTransferDepositoryOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Cash Flow sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def saleTypeOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(saleTypeOptions, stockProfileName=stockProfile)
        objForm = saleTypeOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Cash Flow sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def sectorOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(sectorOptions, stockProfileName=stockProfile)
        objForm = sectorOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Cash Flow sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def subSectorOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(subSectorOptions, stockProfileName=stockProfile)
        objForm = subSectorOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Sub Sector Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def categoryOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(categoryOptions, stockProfileName=stockProfile)
        objForm = categoryOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Category Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def typeOfCompanyOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(typeOfCompanyOptions, stockProfileName=stockProfile)
        objForm = typeOfCompanyOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Type Of Company Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def countryOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(countryOptions, stockProfileName=stockProfile)
        objForm = countryOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Cash Flow sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def managementOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(managementOptions, stockProfileName=stockProfile)
        objForm = managementOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Management Options for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def accountingPracticeOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(accountingPracticeOptions, stockProfileName=stockProfile)
        objForm = accountingPracticeOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Accounting Practice Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def stockOwnershipPatternView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        PHV = request.POST.get('totalPromoterholdingValue')
        MFHV = request.POST.get('mutualFundHoldingValue')
        DIHV = request.POST.get('domesticInstitutionalHoldingsValue')
        FIHV = request.POST.get('foreignInstitutionalHoldingsValue')
        OP = request.POST.get('otherParties')
        total = Decimal(return_val_or_0(PHV)) + Decimal(return_val_or_0(MFHV)) + Decimal(
            return_val_or_0(DIHV)) + Decimal(return_val_or_0(FIHV)) + Decimal(return_val_or_0(OP))
        if Decimal(total) > Decimal(100):
            messages.error(request, 'Sum of entered values can not be more than 100.')
            return redirect(redirectTo)
        if methodType == 'new':
            objlnst = None
            if stockOwnershipPattern.objects.filter(stockProfileName=stockInst, year=enteredYear).exists():
                messages.error(request, 'Values Already Present for Entered Year.')
                return redirect(redirectTo)
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockOwnershipPattern, pk=pkID)
        objForm = stockOwnershipPatternForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Ownership Pattern sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def stockOwnershipPatternPostCall(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        enteredYear = request.data.get('year')
        PHV = request.data.get('totalPromoterholdingValue')
        MFHV = request.data.get('mutualFundHoldingValue')
        DIHV = request.data.get('domesticInstitutionalHoldingsValue')
        FIHV = request.data.get('foreignInstitutionalHoldingsValue')
        OP = request.data.get('otherParties')
        total = Decimal(return_val_or_0(PHV)) + Decimal(return_val_or_0(MFHV)) + Decimal(
            return_val_or_0(DIHV)) + Decimal(return_val_or_0(FIHV)) + Decimal(return_val_or_0(OP))
        if Decimal(total) > Decimal(100):
            # messages.error(request, 'Sum of entered values can not be more than 100.')
            # return redirect(redirectTo)
            return Response({"msg":"Sum of entered values can not be more than 100. !", 'status' : False})
        if methodType == 'new':
            objlnst = None
            if stockOwnershipPattern.objects.filter(stockProfileName=stockInst, year=enteredYear).exists():
                # messages.error(request, 'Values Already Present for Entered Year.')
                # return redirect(redirectTo)
                return Response({"msg":"Values Already Present for Entered Year. !", 'status' : False})
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(stockOwnershipPattern, pk=pkID)
        objForm = stockOwnershipPatternForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({"msg":"stock Events CorpActions sent for verification", "status": True})
        else:
            return Response({"msg":"Error occured while saving the data. Please check the format !", 'status' : False})
        # return redirect(redirectTo)
    return Response({'msg':'Invalid Entry', 'status' : False})

def stockNewsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockNews, pk=pkID)
        objForm = stockNewsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock News sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def websiteMasterView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(websiteMaster, pk=pkID)
        objForm = websiteMasterForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Website  Master sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def stockEventsTypeOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockEventsTypeOptions, stockProfileName=stockProfile)
        objForm = stockEventsTypeOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Events Type Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def dividendTypeOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(dividendTypeOptions, stockProfileName=stockProfile)
        objForm = dividendTypeOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Dividend Type Options for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def stockEventsDividendView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockEventsDividend, pk=pkID)
        objForm = stockEventsDividendForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Events Dividend sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(["POST"])
# @permission_classes((IsAdmin, ))
def stockEventsDividendPostApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(stockEventsDividend, pk=pkID)
        objForm = stockEventsDividendForm(request.data, instance=objlnst)
        if objForm.is_valid():
            print("valid")
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            return Response({'status': 'Stock Events Dividend sent for verification'})
        else:
            return Response({'status': 'Error Occured'})
    return Response({'msg': 'Invalid Entry' })


def corpActionsOptionsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(corpActionsOptions, stockProfileName=stockProfile)
        objForm = corpActionsOptionsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'corp Actions Options sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


## Day 4
# 1 stockSolvency

def stockSolvencyView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockSolvency, stockProfileName=stockProfile)
        objForm = stockSolvencyForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Solvency  sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# stockOperatingEfficiency

def stockOperatingEfficiencyView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockOperatingEfficiency, stockProfileName=stockProfile)
        objForm = stockOperatingEfficiencyForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Operating Efficiency sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# stockRatios

def stockRatiosView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockRatios, stockProfileName=stockProfile)
        objForm = stockRatiosForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Ratios sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# stockPeers
def stockPeersView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockPeers, stockProfileName=stockProfile)
        objForm = stockPeersForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Peers sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['POST'])
def stockPeersApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockPeers, stockProfileName=stockProfile)
        objForm = stockPeersForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            try:
                cd.save()
                cd.refresh_from_db()
            except:
                return Response({'msg':'Description Data already exists kindly update existing data'})
            return Response({'msg':'Data has been sent successfully for verification'})
        else:
            Response({'msg': objForm.errors})
    return Response({'msg':'Invalid Entry'})


#
def financialStatementsFrBalanceSheetView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(financialStatementsFrBalanceSheet, pk=pkID)
        objForm = financialStatementsFrBalanceSheetForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Financial Statements Fr Balance Sheet sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def financialStatementsFrProfitAndLossView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(financialStatementsFrProfitAndLoss, pk=pkID)
        objForm = financialStatementsFrProfitAndLossForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Financial Statements Fr Profit And Loss sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def financialStatementsFrCashFlowView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(financialStatementsFrCashFlow, pk=pkID)
        objForm = financialStatementsFrCashFlowForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Financial Statements Fr Cash Flow sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockGrowthView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockGrowth, stockProfileName=stockProfile)
        objForm = stockGrowthForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Growth sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# ##description field for SEO - starts
def stockFinBalanceSheetSEOView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockFinBalanceSheetSEO, stockProfileName=stockInst)
        objForm = stockFinBalanceSheetSEOForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Financial SEO sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# NEWS
def stockNewsSEOView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockNewsSEO, stockProfileName=stockInst)
        objForm = stockNewsSEOForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock News SEO sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# events
def stockEventsSEOView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockEventsSEO, stockProfileName=stockInst)
        objForm = stockEventsSEOForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Events SEO sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def stockEventsSEOApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockEventsSEO, stockProfileName=stockInst)
        # print(objlnst)
        objForm = stockEventsSEOForm(request.data, instance=objlnst)
        # print(objForm)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            try:
                cd.save()
                cd.refresh_from_db()
            except:
                return Response({'msg':'Details already exists for this stock kindly pass "update" in submit type'})
            return Response({'status':'Stock Events SEO sent for verification'})
        else:
            return Response({'status':'Error Occured'})
    return Response({'msg':'Invalid Entry'})

# description field for SEO - starts

def annualReportsDHRPimageView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            # objlnst = get_object_or_404(annualReportsDHRPImage, stockProfileName=stockProfile)
            objlnst = annualReportsDHRPImage.objects.filter(stockProfileName=stockProfile).last()
        objForm = annualReportsDHRPImageForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'DHRP Report sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def annualReportsDHRPView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(annualReportsDHRP, stockProfileName=stockProfile)
        objForm = annualReportsDHRPForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'DHRP Report sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# def stockDeckAndDocsView(request):
#     if request.method == 'POST':
#         stockProfile = request.POST.get('stockProfile')
#         stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
#         methodType = request.POST.get('submitType')
#         redirectTo = request.POST.get('requestFrom')
#         if methodType == 'new':
#         	objlnst = None
#         else:
#         	pkID = request.POST.get('dataID')
#         	objlnst = get_object_or_404(stockDeckAndDocs, pk=pkID)
#         objForm = stockDeckAndDocsForm(request.POST, request.FILES, instance=objlnst)
#         if objForm.is_valid():
#             cd = objForm.save(commit=False)
#             cd.stockProfileName = stockInst
#             if request.user.is_authenticated:
#                 cd.analyst = request.user
#             cd.save()
#             cd.refresh_from_db()
#             messages.success(request, 'Deck and Docs sent for verification')
#         else:
#             messages.error(request, objForm.errors)
#         return redirect(redirectTo)
#     return HttpResponse('Invalid Entry')


def stockDeckAndDocsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        print(stockProfile)
        # enteredYear = request.POST.get('title')
        if methodType == 'new':
            objlnst = None
        # if financialCompanyUpdates.objects.filter(stockProfileName=stockProfile).exists():
        # 	messages.error(request, 'Values Already Present for Entered Year.')
        # 	return redirect(redirectTo)
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockDeckAndDocs, pk=pkID)
        objForm = stockDeckAndDocsForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Deck and Documents sent for verification')
        else:
            messages.error(request, objForm.errors)



        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def sectorSpecificRatiosView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(sectorSpecificRatios, stockProfileName=stockProfile)
        objForm = sectorSpecificRatiosForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Specific Ratios Description sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
# def peersCompanyLinkingView(request):
# 	if request.method == 'POST':
# 		methodType = request.POST.get('submitType')
# 		stockProfile = request.POST.get('stockProfile')
# 		redirectTo = request.POST.get('requestFrom')
# 		stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
# 		linkedCompCount = peersCompanyLinking.objects.filter(stockProfileName=stockInst).count()
# 		if linkedCompCount < 4:
# 			if methodType == 'new':
# 				objlnst = None
# 			else:
# 				pkID = request.POST.get('dataID')
# 				objlnst = get_object_or_404(peersCompanyLinking, pk=pkID)
# 			objForm = peersCompanyLinkingForm(request.POST, instance=objlnst)
# 			if objForm.is_valid():
# 				cd = objForm.save(commit=False)
# 				cd.stockProfileName = stockInst
# 				if request.user.is_authenticated:
# 					cd.analyst = request.user
# 				cd.save()
# 				cd.refresh_from_db()
# 				messages.success(request, 'Selected Company sent for verification')
# 			else:
# 				messages.error(request, objForm.errors)
# 			return redirect(redirectTo)
# 		else:
# 			messages.error(request, 'Five Companies Already Connected. Delete or Edit previously added entries.')
# 			return redirect(redirectTo)
# 	return HttpResponse('Invalid Entry')

def peersCompanyLinkingView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        stockProfile = request.POST.get('stockProfile')
        redirectTo = request.POST.get('requestFrom')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        if methodType == 'new':
            linkedCompCount = peersCompanyLinking.objects.filter(stockProfileName=stockInst).count()
            if linkedCompCount > 4:
                messages.error(request, 'Five Companies Already Connected. Delete or Edit previously added entries.')
                return redirect(redirectTo)
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(peersCompanyLinking, pk=pkID)
        objForm = peersCompanyLinkingForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Selected Company sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['POST'])
def peersCompanyLinkingApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        methodType = request.data.get('submitType')
        stockProfile = request.data.get('stockProfile')
        redirectTo = request.data.get('requestFrom')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        if methodType == 'new':
            linkedCompCount = peersCompanyLinking.objects.filter(stockProfileName=stockInst).count()
            if linkedCompCount > 4:
                messages.error(request, 'Five Companies Already Connected. Delete or Edit previously added entries.')
                return redirect(redirectTo)
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(peersCompanyLinking, pk=pkID)
        objForm = peersCompanyLinkingForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            try:
                cd.save()
                cd.refresh_from_db()
            except:
                pass
            return Response({'msg':'Selected Company sent for verification'})
        else:
            return Response({'msg': objForm.errors})
    return Response({'msg':'Invalid Entry'})


#
def peersCompanyLinkingForBankNBFCFormView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        stockProfile = request.POST.get('stockProfile')
        redirectTo = request.POST.get('requestFrom')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        if methodType == 'new':
            linkedCompCount = peersCompanyLinkingForBankNBFC.objects.filter(stockProfileName=stockInst).count()
            if linkedCompCount > 4:
                messages.error(request, 'Five Companies Already Connected. Delete or Edit previously added entries.')
                return redirect(redirectTo)
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(peersCompanyLinkingForBankNBFC, pk=pkID)
        objForm = peersCompanyLinkingForBankNBFCForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Selected Company sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def peersCompanyLinkingForBankNBFCFormApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        methodType = request.data.get('submitType')
        stockProfile = request.data.get('stockProfile')
        redirectTo = request.data.get('requestFrom')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        if methodType == 'new':
            linkedCompCount = peersCompanyLinkingForBankNBFC.objects.filter(stockProfileName=stockInst).count()
            if linkedCompCount > 4:
                # messages.error(request, 'Five Companies Already Connected. Delete or Edit previously added entries.')
                return Response({'msg':'Five Companies Already Connected. Delete or Edit previously added entries.'})
            objlnst = None
        else:
            pkID = request.data.get('dataID')
            objlnst = get_object_or_404(peersCompanyLinkingForBankNBFC, pk=pkID)
        objForm = peersCompanyLinkingForBankNBFCForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            try:
                cd.save()
                cd.refresh_from_db()
            except:
                return Response({'msg':'details already exists'})
            return Response({'msg':'Data sent for verification successfully.'})
        else:
            return Response({'msg': objForm.errors})
    return Response({'msg':'Invalid Entry'})


#
def peerLinkingYearlyDataView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        linkToInst = request.POST.get('parentID')
        try:
            parentInst = peersCompanyLinking.objects.get(pk=linkToInst)
        except:
            messages.error(request, 'Please Try Again Later')
            return redirect(redirectTo)
        if methodType == 'new':
            forYear = request.POST.get('year')
            if peerLinkingYearlyData.objects.filter(screenerCompany=parentInst, year=forYear).exists():
                messages.error(request, 'Data for entered Year already exists for Selected Screener Stock.')
                return redirect(redirectTo)
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(peerLinkingYearlyData, pk=pkID)
        objForm = peerLinkingYearlyDataForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.screenerCompany = parentInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data for Entered Year sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')

@api_view(['POST'])
def peerLinkingYearlyDataApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        linkToInst = request.data.get('parentID')
        try:
            parentInst = peersCompanyLinking.objects.get(pk=linkToInst)
        except:
            return Response({'msg': 'Please Try Again Later'})
        if methodType == 'new':
            forYear = request.data.get('year')
            if peerLinkingYearlyData.objects.filter(screenerCompany=parentInst, year=forYear).exists():
                return Response({'msg': 'Data for entered Year already exists for Selected Screener Stock.'})
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(peerLinkingYearlyData, pk=pkID)
        objForm = peerLinkingYearlyDataForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.screenerCompany = parentInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            try:
                cd.save()
                cd.refresh_from_db()
            except:
                return Response({'msg':'Please check some error occured!'})
            return Response({'msg':'Data has been sent successfully for verificatiion'})
        else:
            return Response({'msg': objForm.errors})
    return Response({'msg':'Invalid Entry'})
#
def peerLinkingYearlyDataForBankNBFCView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        linkToInst = request.POST.get('parentID')
        try:
            parentInst = peersCompanyLinkingForBankNBFC.objects.get(pk=linkToInst)
        except:
            messages.error(request, 'Please Try Again Later')
            return redirect(redirectTo)
        if methodType == 'new':
            forYear = request.POST.get('year')
            if peerLinkingYearlyDataForBankNBFC.objects.filter(screenerCompany=parentInst, year=forYear).exists():
                messages.error(request, 'Data for entered Year already exists for Selected Screener Stock.')
                return redirect(redirectTo)
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(peerLinkingYearlyDataForBankNBFC, pk=pkID)
        objForm = peerLinkingYearlyDataForBankNBFCForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.screenerCompany = parentInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data for Entered Year sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['POST'])
def peerLinkingYearlyDataForBankNBFCApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        linkToInst = request.data.get('parentID')
        try:
            parentInst = peersCompanyLinkingForBankNBFC.objects.get(pk=linkToInst)
        except:
            return Response({'msg':'Please Try Again Later'})
        if methodType == 'new':
            forYear = request.data.get('year')
            if peerLinkingYearlyDataForBankNBFC.objects.filter(screenerCompany=parentInst, year=forYear).exists():
                return Response({'msg':'Data for entered Year already exists for Selected Screener Stock.'})
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(peerLinkingYearlyDataForBankNBFC, pk=pkID)
        objForm = peerLinkingYearlyDataForBankNBFCForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.screenerCompany = parentInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            try:
                cd.save()
                cd.refresh_from_db()
            except:
                return Response({'msg':'Yearly linking data for this Stock is already Exists.'})
            return Response({'msg':'Data sent for verifications'})
        else:
            return Response({'msg': objForm.errors})
    return Response({'msg':'Invalid Entry'})


#
def listedRevPeersCompanyLinkingView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        stockProfile = request.POST.get('stockProfile')
        redirectTo = request.POST.get('requestFrom')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        linkedCompCount = peersCompanyLinking.objects.filter(stockProfileName=stockInst).count()
        if linkedCompCount < 3:
            if methodType == 'new':
                objlnst = None
            else:
                objlnst = get_object_or_404(peersCompanyLinking, stockProfileName=stockProfile)
            objForm = listedRevenuePeersCompanyLinkingForm(request.POST, instance=objlnst)
            if objForm.is_valid():
                cd = objForm.save(commit=False)
                cd.stockProfileName = stockInst
                if request.user.is_authenticated:
                    cd.analyst = request.user
                cd.save()
                cd.refresh_from_db()
                messages.success(request, 'Selected Company for Revenue sent for verification')
            else:
                messages.error(request, objForm.errors)
            return redirect(redirectTo)
        else:
            messages.error(request, 'Four Companies Already Connected. Delete or Edit previously added entries.')
            return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def unListedRevPeersCompanyLinkingView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        redirectTo = request.POST.get('requestFrom')
        linkedCompCount = peersCompanyLinking.objects.filter(stockProfileName=stockInst).count()
        tickerVal = request.POST.get('nameIfUnlisted')
        if methodType == 'new':
            objlnst = None
            if linkedCompCount < 3:
                if not peersCompanyLinking.objects.filter(stockProfileName=stockInst, nameIfUnlisted=tickerVal):
                    pass
                else:
                    messages.error(request, 'Company data already present.')
                    return redirect(redirectTo)
            else:
                messages.error(request, 'Four Companies Already Connected. Delete or Edit previously added entries.')
                return redirect(redirectTo)
        else:
            objInst = request.POST.get('instancePK')
            try:
                objlnst = peersCompanyLinking.objects.get(pk=objInst)
            except:
                return HttpResponse('Please Try Again Later')
        objForm = unListedRevenuePeersCompanyLinkingForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Selected Company for Revenue sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def deleteFKdataView(request):
    if request.method == 'POST':
        deletePK = request.POST.get('deleteDataID')
        deleteFrom = request.POST.get('deleteFlag')
        requestedPage = request.POST.get('redirectTo')
        if deleteFrom == 'unlistedCompLinking':
            try:
                objInst = peersCompanyLinking.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'financialStatementsFrBalanceSheet':
            try:
                objInst = financialStatementsFrBalanceSheet.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'financialStatementsFrProfitAndLoss':
            try:
                objInst = financialStatementsFrProfitAndLoss.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'financialStatementsFrCashFlow':
            try:
                objInst = financialStatementsFrCashFlow.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'financialCompanyUpdates':
            try:
                objInst = financialCompanyUpdates.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockDeckAndDocs':
            try:
                objInst = stockDeckAndDocs.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'annualReportsDHRPImage':
            try:
                objInst = annualReportsDHRPImage.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockOwnershipDirector':
            try:
                objInst = stockOwnershipDirector.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'highLights':
            try:
                objInst = highLights.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'deck_images':
            try:
                objInst = deck_images.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockOwnershipInstitutional':
            try:
                objInst = stockOwnershipInstitutional.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockOwnershipPattern':
            try:
                objInst = stockOwnershipPattern.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockNews':
            try:
                objInst = stockNews.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'websiteMaster':
            try:
                objInst = websiteMaster.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockEventsDividend':
            try:
                objInst = stockEventsDividend.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockEventsCorpActions':
            try:
                objInst = stockEventsCorpActions.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockEventsAnnouncements':
            try:
                objInst = stockEventsAnnouncements.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockEventsLegalOrders':
            try:
                objInst = stockEventsLegalOrders.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'peersCompanyLinking':
            try:
                objInst = peersCompanyLinking.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'peersCompanyLinkingForBankNBFC':
            try:
                objInst = peersCompanyLinkingForBankNBFC.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockFundingRounds':
            try:
                objInst = stockFundingRounds.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'industrySpecificGraphs':
            try:
                objInst = industrySpecificGraphs.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'industrySpecificGraphsValues':
            try:
                objInst = industrySpecificGraphsValues.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockBalanceSheet':
            try:
                objInst = stockBalanceSheet.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockCashFlow':
            try:
                objInst = stockCashFlow.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockProfitAndLoss':
            try:
                objInst = stockProfitAndLoss.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockBasicDetail':
            try:
                objInst = stockBasicDetail.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockRevenueBreakUp':
            try:
                objInst = stockRevenueBreakUp.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'bookValueAnnual':
            try:
                objInst = bookValueData.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'stockProfitAndLossTTM':
            try:
                objInst = stockProfitAndLossTTM.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockCashFlowTTM':
            try:
                objInst = stockCashFlowTTM.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockCashFlowTTM':
            try:
                objInst = stockCashFlowTTM.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockBalanceSheetTTM':
            try:
                objInst = stockBalanceSheetTTM.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockBalanceSheetBankNBFCTTM':
            try:
                objInst = stockBalanceSheetBankNBFCTTM.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'stockProfitAndLossBankNBFCTTM':
            try:
                objInst = stockProfitAndLossBankNBFCTTM.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'stockBalanceSheetBankNBFC':
            try:
                objInst = stockBalanceSheetBankNBFC.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockProfitAndLossBankNBFC':
            try:
                objInst = stockProfitAndLossBankNBFC.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'researchReportFAQs':
            try:
                objInst = researchReportFAQs.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'commonFAQ':
            try:
                objInst = commonFAQ.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'totalShareYearlyData':
            try:
                objInst = totalShareYearlyData.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'companyRatios':
            try:
                objInst = companyRatios.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'valuesRBIStandards':
            try:
                objInst = valuesRBIStandards.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'staticPagesSlugs':
            try:
                objInst = staticPagesSlugs.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'redirectBucket':
            try:
                objInst = redirectBucket.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')

        elif deleteFrom == 'blogNews':
            try:
                objInst = blogNews.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
        elif deleteFrom == 'stockListHeading':
            try:
                objInst = stockListHeading.objects.get(pk=deletePK)
                objInst.delete()
                messages.success(request, 'Data Deleted')
            except:
                messages.error(request, 'Please Try Again Later')
                messages.error(request, 'Please Try Again Later')

        return redirect(requestedPage)
    return HttpResponse('Invalid Entry Point')

@api_view(['POST'])
def deleteFKdataAPIView(request):
    if request.method == 'POST' and request.user.is_staff:
        deletePK = request.data.get('deleteDataID')
        deleteFrom = request.data.get('deleteFlag')
        # requestedPage = request.POST.get('redirectTo')
        if deleteFrom == 'unlistedCompLinking':
            try:
                objInst = peersCompanyLinking.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'financialStatementsFrBalanceSheet':
            try:
                objInst = financialStatementsFrBalanceSheet.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'financialStatementsFrProfitAndLoss':
            try:
                objInst = financialStatementsFrProfitAndLoss.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'financialStatementsFrCashFlow':
            try:
                objInst = financialStatementsFrCashFlow.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'financialCompanyUpdates':
            try:
                objInst = financialCompanyUpdates.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockDeckAndDocs':
            try:
                objInst = stockDeckAndDocs.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'annualReportsDHRPImage':
            try:
                objInst = annualReportsDHRPImage.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockOwnershipDirector':
            try:
                objInst = stockOwnershipDirector.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'highLights':
            try:
                objInst = highLights.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'deck_images':
            try:
                objInst = deck_images.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockOwnershipInstitutional':
            try:
                objInst = stockOwnershipInstitutional.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockOwnershipPattern':
            try:
                objInst = stockOwnershipPattern.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockNews':
            try:
                objInst = stockNews.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'websiteMaster':
            try:
                objInst = websiteMaster.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockEventsDividend':
            try:
                objInst = stockEventsDividend.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockEventsCorpActions':
            try:
                objInst = stockEventsCorpActions.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockEventsAnnouncements':
            try:
                objInst = stockEventsAnnouncements.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockEventsLegalOrders':
            try:
                objInst = stockEventsLegalOrders.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'peersCompanyLinking':
            try:
                objInst = peersCompanyLinking.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'peersCompanyLinkingForBankNBFC':
            try:
                objInst = peersCompanyLinkingForBankNBFC.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockFundingRounds':
            try:
                objInst = stockFundingRounds.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'industrySpecificGraphs':
            try:
                objInst = industrySpecificGraphs.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'industrySpecificGraphsValues':
            try:
                objInst = industrySpecificGraphsValues.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockBalanceSheet':
            try:
                objInst = stockBalanceSheet.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockCashFlow':
            try:
                objInst = stockCashFlow.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockProfitAndLoss':
            try:
                objInst = stockProfitAndLoss.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockBasicDetail':
            try:
                objInst = stockBasicDetail.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockRevenueBreakUp':
            try:
                objInst = stockRevenueBreakUp.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'bookValueAnnual':
            try:
                objInst = bookValueData.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'stockProfitAndLossTTM':
            try:
                objInst = stockProfitAndLossTTM.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockCashFlowTTM':
            try:
                objInst = stockCashFlowTTM.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockCashFlowTTM':
            try:
                objInst = stockCashFlowTTM.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockBalanceSheetTTM':
            try:
                objInst = stockBalanceSheetTTM.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockBalanceSheetBankNBFCTTM':
            try:
                objInst = stockBalanceSheetBankNBFCTTM.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'stockProfitAndLossBankNBFCTTM':
            try:
                objInst = stockProfitAndLossBankNBFCTTM.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'stockBalanceSheetBankNBFC':
            try:
                objInst = stockBalanceSheetBankNBFC.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockProfitAndLossBankNBFC':
            try:
                objInst = stockProfitAndLossBankNBFC.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'researchReportFAQs':
            try:
                objInst = researchReportFAQs.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'commonFAQ':
            try:
                objInst = commonFAQ.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'totalShareYearlyData':
            try:
                objInst = totalShareYearlyData.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'companyRatios':
            try:
                objInst = companyRatios.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'valuesRBIStandards':
            try:
                objInst = valuesRBIStandards.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'staticPagesSlugs':
            try:
                objInst = staticPagesSlugs.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'redirectBucket':
            try:
                objInst = redirectBucket.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass

        elif deleteFrom == 'blogNews':
            try:
                objInst = blogNews.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        elif deleteFrom == 'stockListHeading':
            try:
                objInst = stockListHeading.objects.get(pk=deletePK)
                objInst.delete()
                status = True
            except:
                status = False
                pass
        if status == True:
            return Response({'msg': 'Required Item is been deleted','status': status})
        elif status == False:
            return Response({'msg': 'Object ID is not found', 'status': status})

    return Response({'msg': 'Please send the correct request type or the data !','status': False})

def industrySpecificGraphView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(industrySpecificGraphs, pk=pkID)
        objForm = industrySpecificGraphForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Industry Specific Graph sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def industrySpecificGraphValuesView(request):
    if request.method == 'POST':
        graphID = request.POST.get('graphID')
        graphInst = get_object_or_404(industrySpecificGraphs, pk=graphID)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(industrySpecificGraphsValues, pk=pkID)
        objForm = industrySpecificGraphValsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.valuesFor = graphInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Industry Specific Graph Values Added.')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def uploadFinancialFileView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        # methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        objlnst = get_object_or_404(industrySpecificGraphsValues, pk=pkID)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def exporttoCSV(request):
    stockID = request.GET.get('stockID')
    requestedFrom = request.GET.get('requestFor')
    if stockID:
        stock = get_object_or_404(stockBasicDetail, pk=stockID)
        if requestedFrom == 'balanceSheet':
            filteredData = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('year')
            fileName = 'BalanceSheet-stock_' + str(stock.ticker)
            dataset = BalanceSheetResource().export(filteredData)
        elif requestedFrom == 'balanceSheetNBFC':
            filteredData = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
            fileName = 'BalanceSheet-stock_' + str(stock.ticker)
            dataset = BalanceSheetBankNBFCResource().export(filteredData)
        elif requestedFrom == 'stockProfitAndLoss':
            filteredData = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')
            fileName = 'ProfitAndLoss-stock_' + str(stock.ticker)
            dataset = profitAndLossResource().export(filteredData)
        elif requestedFrom == 'stockProfitAndLossNBFC':
            filteredData = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
            fileName = 'ProfitAndLoss-stock_' + str(stock.ticker)
            dataset = profitAndLossBankNBFCResource().export(filteredData)
        elif requestedFrom == 'stockCashFlow':
            filteredData = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')
            fileName = 'CashFlow-stock_' + str(stock.ticker)
            dataset = cashFlowResource().export(filteredData)
        appendYear = '-Years'
        for item in filteredData:
            appendYear += '_' + str(item.year)
        transposeDataSet = dataset.transpose()
        response = HttpResponse(transposeDataSet.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + fileName + appendYear + '.csv"'
        return response
    else:
        return HttpResponse('Invalid Entry')


#
def importFromCSV(request):
    if request.method == 'POST':
        redirectTo = request.POST.get('redirectTo')
        updateModel = request.POST.get('updateFlag')
        untransposeDataSet = Dataset()
        uploadedData = request.FILES['updateFile']
        imported_data = untransposeDataSet.load(uploadedData.read().decode('utf-8'), format='csv')
        dataset = untransposeDataSet.transpose()
        if updateModel == 'stockBalanceSheet':
            result = BalanceSheetResource().import_data(dataset, dry_run=True)
        elif updateModel == 'stockBalanceSheetBankNBFC':
            result = BalanceSheetBankNBFCResource().import_data(dataset, dry_run=True)
        elif updateModel == 'stockProfitAndLoss':
            result = profitAndLossResource().import_data(dataset, dry_run=True)
        elif updateModel == 'stockProfitAndLossBankNBFC':
            result = profitAndLossBankNBFCResource().import_data(dataset, dry_run=True)
        elif updateModel == 'stockCashFlow':
            result = cashFlowResource().import_data(dataset, dry_run=True)
        if not result.has_errors():
            if updateModel == 'stockBalanceSheet':
                BalanceSheetResource().import_data(dataset, dry_run=False)
            elif updateModel == 'stockBalanceSheetBankNBFC':
                BalanceSheetBankNBFCResource().import_data(dataset, dry_run=False)
            elif updateModel == 'stockProfitAndLoss':
                profitAndLossResource().import_data(dataset, dry_run=False)
            elif updateModel == 'stockProfitAndLossBankNBFC':
                profitAndLossBankNBFCResource().import_data(dataset, dry_run=False)
            elif updateModel == 'stockCashFlow':
                cashFlowResource().import_data(dataset, dry_run=False)
            messages.success(request, 'Data Uploaded/Updated.')
        else:
            messages.error(request, 'Error Occured. Error: ' + str(result))
        return redirect(redirectTo)
    else:
        return HttpResponse('Invalid Entry')


#
class newsJSONListView(View):
    def get(self, *args, **kwargs):
        upper = kwargs.get('num_posts')
        lower = upper - 5
        posts = list(stockNews.objects.values())[lower:upper]
        posts_size = len(stockNews.objects.all())
        size = True if upper >= posts_size else False
        return JsonResponse({'data': posts, 'max': size}, safe=False)


#
def pubDraftActionView(request):
    if request.method == 'POST':
        try:
            stockProfile = request.POST.get('stockProfile')
            stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
            objForm = pubDraftStockForm(request.POST, instance=stockInst)
            if objForm.is_valid():
                cd = objForm.save(commit=False)
                cd.verifiedBy = request.user
                cd.save()
                cd.refresh_from_db()
                messages.success(request, 'Stock Updated')
            else:
                messages.error(request, objForm.errors)
        except:
            messages.error(request, 'Err.. Please Try Again Later.')
        return redirect('stockApp:stockListURL')
    return HttpResponse('Invalid Entry')


#
def foundingRoundsFigureUnitsView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(foundingRoundsFigureUnits, stockProfileName=stockProfile)
        objForm = foundingRoundsFigureUnitsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Founding Rounds Figure Units Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
#
def fundingDetailsVisibilityView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(fundingDetailsVisibility, stockProfileName=stockProfile)
        objForm = fundingDetailsVisibilityForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def benGrahamOrDCFView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(benGrahamOrDCF, stockProfileName=stockProfile)
        objForm = benGrahamOrDCFForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
from videoBlogApp.models import videoBlogHits, blogVideos


def testPageView(request):
    videos = blogVideos.objects.all()
    trending = {}
    for item in videos:
        videoHits = videoBlogHits.objects.filter(videoBlog=item, \
                                                 created__lte=datetime.datetime.today(), \
                                                 created__gt=datetime.datetime.today() - datetime. \
                                                 timedelta(days=30)).count()
        trending[item] = videoHits
    context = {
        'trending': trending,
    }
    return render(request, 'UI/testPage.html', context)


#
def stockBalanceSheetTTMView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        # if not stockBalanceSheetTTM.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockBalanceSheetTTM, pk=pkID)
        objForm = stockBalanceSheetTTMForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock BalanceSheet TTM sent for verification')
        else:
            messages.error(request, objForm.errors)
        # else:
        # 	messages.error(request, 'Values Already Present for Entered Year.')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockProfitAndLossTTMView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        # if not stockBalanceSheetTTM.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockProfitAndLossTTM, pk=pkID)
        objForm = stockProfitAndLossTTMForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Profit and Loss TTM sent for verification')
        else:
            messages.error(request, objForm.errors)
        # else:
        # 	messages.error(request, 'Values Already Present for Entered Year.')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockCashFlowTTMView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        # if not stockBalanceSheetTTM.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockCashFlowTTM, pk=pkID)
        objForm = stockCashFlowTTMForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Cash Flow TTM sent for verification')
        else:
            messages.error(request, objForm.errors)
        # else:
        # 	messages.error(request, 'Values Already Present for Entered Year.')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def stockBalanceSheetBankNBFCTTMView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        print(stockProfile)
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        print(stockInst)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        # if not stockBalanceSheetTTM.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockBalanceSheetBankNBFCTTM, pk=pkID)
        objForm = stockBalanceSheetBankNBFCTTMForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock BalanceSheet TTM sent for verification')
        else:
            messages.error(request, objForm.errors)
        # else:
        # 	messages.error(request, 'Values Already Present for Entered Year.')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


def stockProfitAndLossBankNBFCTTMView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        print(stockProfile)
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        print(stockInst)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        enteredYear = request.POST.get('year')
        # if not stockBalanceSheetTTM.objects.filter(stockProfileName=stockProfile, year=enteredYear).exists():
        if methodType == 'new':
            objlnst = None
        else:
            pkID = request.POST.get('dataID')
            objlnst = get_object_or_404(stockProfitAndLossBankNBFCTTM, pk=pkID)
        objForm = stockProfitAndLossBankNBFCTTMForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Stock Profit and Loss TTM sent for verification')
        else:
            messages.error(request, objForm.errors)
        # else:
        # 	messages.error(request, 'Values Already Present for Entered Year.')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


# For Bank NBFC's Templates starts

# doubts pen down
def stockBalanceSheetCalculationForBankNBFc(stock):
    # balanceSheetSolvency = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')[0:7]
    balanceSheetSolvency = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')[0:10]
    blYearList = []
    deRatio = {}
    currentRatio = {}
    quickRatio = {}
    avgROceDenoPart = {}
    averageTotalEquityDict = {}
    avgTotalLongTermDebtDict = {}
    avgIntangibleAssetDict = {}
    avgTotalAssetDict = {}
    for item in balanceSheetSolvency:
        blYearList.append(item.year)
    yearListLen = len(blYearList)
    for i in range(yearListLen):
        if (i + 1) < yearListLen:
            CYear = blYearList[i]
            PYear = blYearList[i + 1]
            CYMain = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=CYear)
            PYMain = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=PYear)

            # longtermborrowings
            if CYMain.longTermBorrowings:
                longTermBorrCY = CYMain.longTermBorrowings
            else:
                longTermBorrCY = 0

            if PYMain.longTermBorrowings:
                longTermBorrPY = PYMain.longTermBorrowings
            else:
                longTermBorrPY = 0

            # shorttermborrowings
            if CYMain.shortTermBorrowings:
                shortTermBorrCY = CYMain.shortTermBorrowings
            else:
                shortTermBorrCY = 0

            if PYMain.shortTermBorrowings:
                shortTermBorrPY = PYMain.shortTermBorrowings
            else:
                shortTermBorrPY = 0

            # currentportionoflongtermdebt
            if CYMain.currentPortionOfLongTermDebt:
                currPortLnTermDebtCY = CYMain.currentPortionOfLongTermDebt
            else:
                currPortLnTermDebtCY = 0

            if PYMain.currentPortionOfLongTermDebt:
                currPortLnTermDebtPY = PYMain.currentPortionOfLongTermDebt
            else:
                currPortLnTermDebtPY = 0

            # leaseliabilities
            if CYMain.leaseLiability:
                leaseLiabilityCY = CYMain.leaseLiability
            else:
                leaseLiabilityCY = 0

            if PYMain.leaseLiability:
                leaseLiabilityPY = PYMain.leaseLiability
            else:
                leaseLiabilityPY = 0

            # --------------no use starts -------------------
            # if CYMain.longTermPortionOfLeases: #dount3
            # 	lnTermPortionOfLeasesCY = CYMain.longTermPortionOfLeases
            # else:
            # 	lnTermPortionOfLeasesCY = 0

            # if PYMain.longTermPortionOfLeases:
            # 	lnTermPortionOfLeasesPY = PYMain.longTermPortionOfLeases
            # else:
            # 	lnTermPortionOfLeasesPY = 0
            # --------------no use ends -------------------

            totalLnDebtCY = longTermBorrCY + shortTermBorrCY + currPortLnTermDebtCY + leaseLiabilityCY
            totalLnDebtPY = longTermBorrPY + shortTermBorrPY + currPortLnTermDebtPY + leaseLiabilityPY

            if CYMain.totalEquity:
                totalEquityCY = CYMain.totalEquity
            else:
                totalEquityCY = 0
            if PYMain.totalEquity:
                totalEquityPY = PYMain.totalEquity
            else:
                totalEquityPY = 0

            # if CYMain.currentAssets:
            # 	currentAssetsCY = CYMain.currentAssets
            # else:
            # 	currentAssetsCY = 0
            # if PYMain.currentAssets:
            # 	currentAssetsPY = PYMain.currentAssets
            # else:
            # 	currentAssetsPY = 0

            # cashandcashequivalents
            if CYMain.cashAndCashEquivalents:
                cashEquivalentsCY = CYMain.cashAndCashEquivalents
            else:
                cashEquivalentsCY = 0
            if PYMain.cashAndCashEquivalents:
                cashEquivalentsPY = PYMain.cashAndCashEquivalents
            else:
                cashEquivalentsPY = 0

            # otherRecieveables
            if CYMain.otherReceivables:
                otherReceivablesCY = CYMain.otherReceivables
            else:
                otherReceivablesCY = 0
            if PYMain.otherReceivables:
                otherReceivablesPY = PYMain.otherReceivables
            else:
                otherReceivablesPY = 0

            # otherCurrentAssests
            if CYMain.otherCurrentAssets:
                otherCurrentAssetsCY = CYMain.otherCurrentAssets
            else:
                otherCurrentAssetsCY = 0
            if PYMain.otherCurrentAssets:
                otherCurrentAssetsPY = PYMain.otherCurrentAssets
            else:
                otherCurrentAssetsPY = 0

            # currentAssests
            currentAssetsCY = cashEquivalentsCY + otherReceivablesCY + otherCurrentAssetsCY
            currentAssetsPY = cashEquivalentsPY + otherReceivablesPY + otherCurrentAssetsPY

            # tradePayable
            if CYMain.tradePayable:
                tradePayableCY = CYMain.tradePayable
            else:
                tradePayableCY = 0
            if PYMain.tradePayable:
                tradePayablePY = PYMain.tradePayable
            else:
                tradePayablePY = 0

            #

            # otherCurrLiabilities
            if CYMain.otherCurrentLiabilities:
                otherCurrLiabilitiesCY = CYMain.otherCurrentLiabilities
            else:
                otherCurrLiabilitiesCY = 0
            if PYMain.otherCurrentLiabilities:
                otherCurrLiabilitiesPY = PYMain.otherCurrentLiabilities
            else:
                otherCurrLiabilitiesPY = 0

            currentLiabCY = tradePayableCY + otherCurrLiabilitiesCY
            currentLiabPY = tradePayablePY + otherCurrLiabilitiesPY

            # if CYMain.currentLiabilities:#doubt 5
            # 	currentLiabCY = CYMain.currentLiabilities
            # else:
            # 	currentLiabCY = 0
            # if PYMain.currentLiabilities:
            # 	currentLiabPY = PYMain.currentLiabilities
            # else:
            # 	currentLiabPY = 0

            # nonCurrentLiabilities starts - no use
            # if CYMain.nonCurrentLiabilities:
            # 	nonCurrentLiabCY = CYMain.nonCurrentLiabilities
            # else:
            # 	nonCurrentLiabCY = 0
            # if PYMain.nonCurrentLiabilities:
            # 	nonCurrentLiabPY = PYMain.nonCurrentLiabilities
            # else:
            # 	nonCurrentLiabPY = 0
            # nonCurrentLiabilities ends - no use

            if CYMain.totalInventory:
                totInvCY = CYMain.totalInventory
            else:
                totInvCY = 0

            if PYMain.totalInventory:
                totInvPY = PYMain.totalInventory
            else:
                totInvPY = 0

            if CYMain.totalAssets:
                totalAssetsCY = CYMain.totalAssets
            else:
                totalAssetsCY = 0

            if PYMain.totalAssets:
                totalAssetsPY = PYMain.totalAssets
            else:
                totalAssetsPY = 0

            # if CYMain.prepaidExpenses: #doubt7
            # 	prepaidExpCY = CYMain.prepaidExpenses
            # else:
            # 	prepaidExpCY = 0
            # if PYMain.prepaidExpenses:
            # 	prepaidExpPY = PYMain.prepaidExpenses
            # else:
            # 	prepaidExpPY = 0

            # if CYMain.nonCurrentAssets: #doubt8 ( Is this non financial assest)
            # 	nonCurrentAssetsCY = CYMain.nonCurrentAssets
            # else:
            # 	nonCurrentAssetsCY = 0
            # if PYMain.nonCurrentAssets:
            # 	nonCurrentAssetsPY = PYMain.nonCurrentAssets
            # else:
            # 	nonCurrentAssetsPY = 0

            # no use
            # if CYMain.otherIntangibleAssests:
            # 	othrIntangAssestsCY = CYMain.otherIntangibleAssests
            # else:
            # 	othrIntangAssestsCY = 0
            # if PYMain.otherIntangibleAssests:
            # 	othrIntangAssestsPY = PYMain.otherIntangibleAssests
            # else:
            # 	othrIntangAssestsPY = 0

            # totalCalculatedLnDebtCY = totalLnDebtCY + currPortLnTermDebtCY + currPortLeasesCY + lnTermPortionOfLeasesCY
            # totalCalculatedLnDebtPY = totalLnDebtPY + currPortLnTermDebtPY + currPortLeasesPY + lnTermPortionOfLeasesPY

            # As per Ishima - currPortLeasesCY and lnTermPortionOfLeasesCY means leaseLiabilityCY starts
            totalCalculatedLnDebtCY = totalLnDebtCY + currPortLnTermDebtCY + leaseLiabilityCY
            totalCalculatedLnDebtPY = totalLnDebtPY + currPortLnTermDebtPY + leaseLiabilityPY
            # As per Ishima - currPortLeasesCY and lnTermPortionOfLeasesCY means leaseLiabilityCY ends

            # avgCalculatedNonLiabilities = (nonCurrentLiabCY + nonCurrentLiabPY) / Decimal(2)
            avgTotalLongTermDebt = (totalCalculatedLnDebtCY + totalCalculatedLnDebtPY) / Decimal(2)
            avgTotalEquity = (totalEquityCY + totalEquityPY) / Decimal(2)
            avgCurrentAsset = (currentAssetsCY + currentAssetsPY) / Decimal(2)

            avgTotalAsset = (totalAssetsCY + totalAssetsPY) / Decimal(2)

            # avgNonCurrentAsset = (nonCurrentAssetsCY + nonCurrentAssetsPY) / Decimal(2)
            avgCurrentLiabilities = (currentLiabCY + currentLiabPY) / Decimal(2)
            avgInventory = (totInvCY + totInvPY) / Decimal(2)
            # avgPrepaidExpenses = (prepaidExpCY + prepaidExpPY) / Decimal(2)
            # avgIntangibleAsset = (othrIntangAssestsCY + othrIntangAssestsPY ) / Decimal(2)

            if avgTotalEquity == 0:
                avgTotalEquity = 1

            if avgCurrentLiabilities == 0:
                avgCurrentLiabilities = 1

            deRatio[CYear] = round((avgTotalLongTermDebt / avgTotalEquity), 2)
            currentRatio[CYear] = round((avgCurrentAsset / avgCurrentLiabilities), 2)

            # ishima asked to remove prepaid expenses from formula starts
            # quickRatio[CYear] = round(((avgCurrentAsset - avgInventory + avgPrepaidExpenses ) / avgCurrentLiabilities),2)
            quickRatio[CYear] = round(((avgCurrentAsset - avgInventory) / avgCurrentLiabilities), 2)
            # ishima asked to remove prepaid expenses from formula ends

            # changes related to Kulmehar report starts
            # averageTotalEquityDict[CYear] = round(avgTotalEquity,2)
            # changes related to Kulmehar report ends

            averageTotalEquityDict[CYear] = avgTotalEquity

            avgTotalLongTermDebtDict[CYear] = round(avgTotalLongTermDebt, 2)

            # changes related to Kulmehar report starts
            # avgTotalAssetDict[CYear] = round(avgCurrentAsset + avgNonCurrentAsset,2)
            # changes related to Kulmehar report ends

            # avgTotalAssetDict[CYear] = avgCurrentAsset + avgNonCurrentAsset
            avgTotalAssetDict[CYear] = avgTotalAsset  # (Ishima said non current assest nhi hota Bank & NBFC mein)

            # changes related to Kulmehar report starts
            # avgIntangibleAssetDict[CYear] = round(avgIntangibleAsset,2)
            # changes related to Kulmehar report ends

            # avgIntangibleAssetDict[CYear] = avgIntangibleAsset

            # Ishima ROCE formula denominator changes starts
            # avgROceDenoPart[CYear] = round(avgCalculatedNonLiabilities,2)
            avgROceDenoPart[CYear] = round(avgCurrentLiabilities, 2)
        # Ishima ROCE formula denominator changes ends

    return deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgROceDenoPart


#
# doubts pen down
def stockProfitAndLossCalculationForBankNBFc(stock, callingFunction=0):
    interestCoverageRatio = {}
    operatingProfitEBITmargin = {}
    pbtMargin = {}
    patMargin = {}
    netIncomeDict = {}
    netIncomeSnapShotDict = {}
    pbitDict = {}
    revenueDict = {}
    # profitLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:7]
    profitLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:10]

    forCount = 0
    for item in profitLoss:
        forCount += 1
        if item.pbit:
            pbitCal = item.pbit
        else:
            pbitCal = 1

        # doubt2 (Under discussion)
        # if item.interestExpense:
        # 	interestExpCal = item.interestExpense
        # else:
        # 	interestExpCal = 1
        interestExpCal = 1
        # doubt2 (Under discussion)

        if item.netInterestIncome:  # doubt3 (net Interest Income is revenue of operations as per Ishima)
            revenueOnlyCal = item.netInterestIncome
        else:
            revenueOnlyCal = 1

        if item.pbt:
            pbtCal = item.pbt
        else:
            pbtCal = 1
        if item.netIncome:
            netIncomeCal = item.netIncome
        else:
            netIncomeCal = 1
        if item.totalRevenue:
            revenueCal = item.totalRevenue
        else:
            revenueCal = 1

        interestCoverageRatio[item.year] = round((pbitCal / interestExpCal), 2)
        operatingProfitEBITmargin[item.year] = round((pbitCal / revenueOnlyCal) * 100, 2)
        pbtMargin[item.year] = round((pbtCal / revenueOnlyCal) * 100, 2)
        patMargin[item.year] = round((netIncomeCal / revenueOnlyCal) * 100, 2)
        # changes from Kulmeher report starts
        # netIncomeDict[item.year] = round(netIncomeCal,2)
        # changes from Kulmeher report ends
        netIncomeDict[item.year] = netIncomeCal

        netIncomeSnapShotDict[forCount] = round(netIncomeCal, 2)
        pbitDict[item.year] = round(pbitCal, 2)
        revenueDict[item.year] = round(revenueCal, 2)
    if callingFunction == 'snapshot':
        return revenueDict, netIncomeSnapShotDict
    else:
        return interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict


#
def calGrowthTemplateDataViewFrBankNBFcs(stock, requestFrom=None):
    returnRevenueGrowthData = {}
    returnRevenueGrowthAlgoProgrammedData = {}
    returnNetProfitGrowthData = {}
    returnNetProfitAlgoProgrammedData = {}
    returnEPSGrowthData = {}
    returnEPSAlgoProgrammedData = {}
    returnEBITDAGrowthData = {}
    returnEBITDAAlgoProgrammedData = {}
    returnPBITGrowthData = {}
    returnPBITAlgoProgrammedData = {}
    totalYearsData = []
    totalData = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')
    for item in totalData:
        totalYearsData.append(item.year)
    if (len(totalYearsData) > 1):
        CYear = totalYearsData[0]
        CY = stockProfitAndLossBankNBFC.objects.get(stockProfileName=stock, year=CYear)
        for i, j in enumerate(totalYearsData[:-1]):
            forloopCounter = i + 1
            firstYear = j
            prevYear = totalYearsData[i + 1]
            n = CYear - prevYear
            PY = stockProfitAndLossBankNBFC.objects.get(stockProfileName=stock, year=prevYear)
            # revenue
            calculatedRevGrowth = (calGrowthFormulaView(CY.totalRevenue, PY.totalRevenue, n))
            if calculatedRevGrowth:
                returnRevenueGrowthData[n] = calculatedRevGrowth
                # revenueForGrowth
                returnRevenueGrowthAlgoProgrammedData[forloopCounter] = calculatedRevGrowth
            # PAT
            CYEBITDA = return_val_or_0(CY.ebidta)
            CYPBIT = return_val_or_0(CY.pbit)
            CYPBT = return_val_or_0(CY.pbt)
            CYPAT = return_val_or_0(CY.netIncome)
            PYEBITDA = return_val_or_0(PY.ebidta)
            PYPBIT = return_val_or_0(PY.pbit)
            PYPBT = return_val_or_0(PY.pbt)
            PYPAT = return_val_or_0(PY.netIncome)
            calculatedPATGrowth = (calGrowthFormulaView(CYPAT, PYPAT, n))
            if calculatedPATGrowth:
                returnNetProfitGrowthData[n] = calculatedPATGrowth
                # PATForGrowth
                returnNetProfitAlgoProgrammedData[forloopCounter] = calculatedPATGrowth
            # EPS
            CYEps = return_val_or_0(CY.basicEPS)
            PYEps = return_val_or_0(PY.basicEPS)
            calculatedEPSGrowth = (calGrowthFormulaView(CYEps, PYEps, n))
            if calculatedEPSGrowth:
                returnEPSGrowthData[n] = calculatedEPSGrowth
                # EPSForGrowth
                returnEPSAlgoProgrammedData[forloopCounter] = calculatedEPSGrowth
            # EBITDA
            calculatedEBITDAGrowth = (calGrowthFormulaView(CYEBITDA, PYEBITDA, n))
            if calculatedEBITDAGrowth:
                returnEBITDAGrowthData[n] = calculatedEBITDAGrowth
                # EBITDAForGrowth
                returnEBITDAAlgoProgrammedData[forloopCounter] = calculatedEBITDAGrowth
            # PBIT

            calculatedPBITGrowth = (calGrowthFormulaView(CYPBIT, PYPBIT, n))
            if calculatedPBITGrowth:
                returnPBITGrowthData[n] = calculatedPBITGrowth
                # PBITForGrowth
                returnPBITAlgoProgrammedData[forloopCounter] = calculatedPBITGrowth
    if requestFrom == 'snapshot':
        return returnRevenueGrowthData, returnNetProfitAlgoProgrammedData
    else:
        return returnRevenueGrowthData, returnRevenueGrowthAlgoProgrammedData, returnNetProfitGrowthData, returnNetProfitAlgoProgrammedData, returnEPSGrowthData, returnEPSAlgoProgrammedData, returnEBITDAGrowthData, returnEBITDAAlgoProgrammedData, returnPBITGrowthData, returnPBITAlgoProgrammedData


#
def growthCalculatorForAnnualValuesFrBankNBFCs(stock, growthFor='bookValue'):
	if growthFor == 'bookValue':
		objs = bookValueData.objects.filter(stockProfileName=stock).order_by('-year')[0:]
	elif growthFor == 'assetGrowth':
		objs = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')[0:]
	elif growthFor == 'cashFlow':
		objs = stockCashFlow.objects.filter(stockProfileName=stock).order_by('-year')[0:]
	valDict = {}
	valDictFinancing = {}
	totalYearsData = []
	for item in objs:
		totalYearsData.append(item.year)
	if (len(totalYearsData) > 1):
		CYear = totalYearsData[0]
		if growthFor == 'bookValue':
			CY = bookValueData.objects.get(stockProfileName=stock, year=CYear)
		elif growthFor == 'assetGrowth':
			CY = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=CYear)
		elif growthFor == 'cashFlow':
			CY = stockCashFlow.objects.get(stockProfileName=stock, year=CYear)
	totalShareOutstanding = {}
	bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('-year')[0:]
	for item in bookValuesObjs:
		totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=item.year)
		totalShareOutstanding[item.year] = totalShareOutStandValueObj.totalCommonSharesOutstanding
	for i, j in enumerate(totalYearsData[:-1]):
		forloopCounter = i + 1
		firstYear = j
		prevYear = totalYearsData[i + 1]
		n = CYear - prevYear
		if growthFor == 'bookValue':		
			PY = bookValueData.objects.get(stockProfileName=stock, year=prevYear)
			calculatedValGrowth = calGrowthFormulaView((CY.bookValue/totalShareOutstanding[CY.year]), (PY.bookValue/totalShareOutstanding[PY.year]), n)
			# PY = bookValueData.objects.get(stockProfileName=stock, year=prevYear)
			# calculatedValGrowth = calGrowthFgormulaView(CY.bookValue, PY.bookValue, n)
		elif growthFor == 'assetGrowth':
			PY = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=prevYear)
			calculatedValGrowth = calGrowthFormulaView(CY.totalAssets, PY.totalAssets, n)
		elif growthFor == 'cashFlow':
			PY = stockCashFlow.objects.get(stockProfileName=stock, year=prevYear)
			calculatedValGrowth = calGrowthFormulaView(CY.cashFromOperatingActivities, PY.cashFromOperatingActivities,
													   n)
			calculatedValGrowthFinancing = calGrowthFormulaView(CY.cashFromFinancingActivities,
																PY.cashFromFinancingActivities, n)
		if calculatedValGrowth:
			valDict[forloopCounter] = calculatedValGrowth
		if growthFor == 'cashFlow':
			valDictFinancing[forloopCounter] = calculatedValGrowthFinancing
	processedDict = calculateProgrammedGrowth(valDict)
	if growthFor == 'cashFlow':
		processedDictFinancing = calculateProgrammedGrowth(valDictFinancing)
		return processedDict, processedDictFinancing
	else:
		return processedDict




#
# def ROEgrowthCalculatorFrBankNBFCs(stock):
# 	profitAndLossObjs = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')
# 	totalYearsData = []
# 	ROEDict = {}
# 	netIncomeCY = None
# 	totalEquityCY = None
# 	totalEquityPY = None
# 	for item in profitAndLossObjs:
# 		totalYearsData.append(item.year)
# 	if (len(totalYearsData) > 1):
# 		forloopCounter = 0
# 		for i, j in enumerate(totalYearsData[:-1]):
# 			forloopCounter += 1
# 			firstYear = j
# 			prevYear = totalYearsData[i+1]
# 			CYProfLoss = stockProfitAndLossBankNBFC.objects.get(stockProfileName=stock, year=firstYear)
# 			try:
# 				CYBalanceSheet = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=firstYear)
# 			except:
# 				CYBalanceSheet = 0
# 			try:
# 				PYBalanceSheet = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=prevYear)
# 			except:
# 				PYBalanceSheet = 0
# 			if CYProfLoss.netIncome:
# 				netIncomeCY = Decimal(CYProfLoss.netIncome)
# 			if CYBalanceSheet:
# 				if CYBalanceSheet.totalEquity:
# 					totalEquityCY = CYBalanceSheet.totalEquity
# 			if PYBalanceSheet:
# 				if PYBalanceSheet.totalEquity:
# 					totalEquityPY = PYBalanceSheet.totalEquity
# 			calculatedROE = ROEFormula(netIncomeCY,totalEquityCY,totalEquityPY)
# 			ROEDict[forloopCounter] = calculatedROE
# 			ROEDict = calculateProgrammedGrowth(ROEDict)
# 		return ROEDict
# 	else:
# 		return False

#
def ROEgrowthCalculatorFrBankNBFCs(stock):
    profitAndLossObjs = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')
    totalYearsData = []
    roeList = []
    ROEDict = {}
    netIncomeCY = None
    totalEquityCY = None
    totalEquityPY = None
    for item in profitAndLossObjs:
        totalYearsData.append(item.year)
    if (len(totalYearsData) > 1):
        forloopCounter = 0
        for i, j in enumerate(totalYearsData[:-1]):
            forloopCounter += 1
            firstYear = j
            prevYear = totalYearsData[i + 1]
            CYProfLoss = stockProfitAndLossBankNBFC.objects.get(stockProfileName=stock, year=firstYear)
            try:
                CYBalanceSheet = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=firstYear)
            except:
                CYBalanceSheet = 0
            try:
                PYBalanceSheet = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=prevYear)
            except:
                PYBalanceSheet = 0
            if CYProfLoss.netIncome:
                netIncomeCY = Decimal(CYProfLoss.netIncome)
            if CYBalanceSheet:
                if CYBalanceSheet.totalEquity:
                    totalEquityCY = CYBalanceSheet.totalEquity
            if PYBalanceSheet:
                if PYBalanceSheet.totalEquity:
                    totalEquityPY = PYBalanceSheet.totalEquity
            calculatedROE = ROEFormula(netIncomeCY, totalEquityCY, totalEquityPY)
            ROEDict[firstYear] = calculatedROE
            roeObj = roeSelfObj(year=firstYear, value=calculatedROE)
            roeList.append(roeObj)
        ROEDictNew = calculateForListGrowthNewRoe(roeList, 'roe')

        return ROEDictNew
    else:
        return False


#
def intrinsicFormulafrBankNBFCs(stock):
    calVal = None
    try:
        lastestBondRateObj = currentRateOfbondYield.objects.latest('id')
        lastestBondRate = lastestBondRateObj.value
    except:
        lastestBondRate = None
    if lastestBondRate:
        try:
            stockEssObj = stockEssentials.objects.get(stockProfileName=stock)
            salesGrowthRateOfXYearVal = stockEssObj.salesGrowthRateOfXYear
        except:
            salesGrowthRateOfXYearVal = None
        try:
            stockProfLossObj = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            dilutedEps = stockProfLossObj.dilutedEPS
            basicEps = stockProfLossObj.basicEPS
        except:
            basicEps = dilutedEps = None
        eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
        if salesGrowthRateOfXYearVal:
            if eps:
                calVal = eps * (Decimal(8.5) + (Decimal(2) * salesGrowthRateOfXYearVal)) * (
                        Decimal(8.5) / lastestBondRate)
                calVal = round(calVal, 2)
    return calVal


# doubts mentioned in comment
def snapshotForBankNBFCsView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    print(f'NBFC snap Hit: {stock}')
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    callingFunction = 'snapshot'
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None
    createStockAdmin = stockAdminForm(instance=stockAdmInst)
    createStockAdminSnapshot = stockAdminSnapshotForm(instance=stockAdmInst)

    try:
        benGrahamOrDCFInst = benGrahamOrDCF.objects.get(stockProfileName=stock)
    except:
        benGrahamOrDCFInst = None
    benGrahamOrDCFCreate = benGrahamOrDCFForm(instance=benGrahamOrDCFInst)

    try:
        essentialInst = stockEssentials.objects.get(stockProfileName=stock)
    except:
        essentialInst = None
    createStockEssentials = stockEssentialsForm(instance=essentialInst)
    createStockEssentialsBottom = stockEssentialsBottomForm(instance=essentialInst)

    try:
        stockInvestmentChecklistInst = stockInvestmentChecklist.objects.get(stockProfileName=stock)
    except:
        stockInvestmentChecklistInst = None
    createstockInvestmentChecklist = stockInvestmentChecklistForm(instance=stockInvestmentChecklistInst)

    try:
        stockIPOInst = stockIPO.objects.get(stockProfileName=stock)
    except:
        stockIPOInst = None
    createStockIPO = stockIPOForm(instance=stockIPOInst)

    try:
        stockDetailsInst = stockDetails.objects.get(stockProfileName=stock)
    except:
        stockDetailsInst = None
    createStockDetails = stockDetailsFormMergerAcquistion(instance=stockDetailsInst)
    createSubsidiariesBusModelStockDetails = stockDetailsSubsidiariesBusModelForm(instance=stockDetailsInst)
    createProductStockDetails = stockDetailsProductForm(instance=stockDetailsInst)
    createAssestStockDetails = stockDetailsAssestForm(instance=stockDetailsInst)
    createIndustryOverviewStockDetails = stockDetailsIndustryOverviewForm(instance=stockDetailsInst)
    createStockAbout = stockDetailsAboutForm(instance=stockDetailsInst)
    createawardsDescription = stockDetailsAwardForm(instance=stockDetailsInst)
    createSSOTDescription = stockDetailsSSOTForm(instance=stockDetailsInst)

    revenueBreakupInst = stockRevenueBreakUp.objects.filter(stockProfileName=stock)
    viewStockRevenueBreakUpForm = stockRevenueBreakUpForm()

    try:
        stockFundingInst = stockFunding.objects.get(stockProfileName=stock)
    except:
        stockFundingInst = None
    createStockFunding = stockFundingForm(instance=stockFundingInst)

    stockFundingRoundsInst = stockFundingRounds.objects.filter(stockProfileName=stock).order_by('-dateOfInvestment')
    createStockFundingRounds = stockFundingRoundsForm()

    try:
        promotorHolding = stockOwnershipPattern.objects.get(stockProfileName=stock, year=currentYear)
        promotorHolding = promotorHolding.totalPromoterholdingValue
    except:
        promotorHolding = None
    try:
        # latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
        latestProfitAndLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')

        totalRevCY = latestProfitAndLoss.totalRevenue
        patCY = latestProfitAndLoss.netIncome
        epsCY = latestProfitAndLoss.basicEPS
        dps = latestProfitAndLoss.DPS
    except:
        totalRevCY = None
        patCY = None
        epsCY = None
        dps = None
    try:
        latestCashFlow = stockCashFlow.objects.filter(stockProfileName=stock).latest('year')
        cashFlowOperationsCY = latestCashFlow.cashFromOperatingActivities
        cashFlowFinancingCY = latestCashFlow.cashFromFinancingActivities
    except:
        cashFlowOperationsCY = None
        cashFlowFinancingCY = None

    categoryForEss = categoryOptions.objects.all().order_by('name')
    sectorForEss = sectorOptions.objects.all().order_by('name')
    subSectorForEss = subSectorOptions.objects.all().order_by('name')

    # Required changes in formuals Calculation starts  - done
    returnedGrowthROEVal = ROEgrowthCalculatorFrBankNBFCs(stock)
    intrinsicVal = intrinsicFormula(stock, forNBFC=True)
    # intrinsicVal = intrinsicFormulafrBankNBFCs(stock)
    returnedRevenueGrowthAlgoProgrammedData, processedNetProfitGrowthTextual = calGrowthTemplateDataViewFrBankNBFcs(
        stock, requestFrom='snapshot')
    # compoundSalesGrowth = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    # compoundProfitGrowth = calculateProgrammedGrowth(processedNetProfitGrowthTextual)
    profitAndLossQuerySet = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')
    revenueGrowth = calculateGrowthNew(profitAndLossQuerySet, 'totalRevenue')
    compoundProfitGrowth = calculateGrowthNew(profitAndLossQuerySet, 'netIncome')
    # Required changes in formuals Calculation ends - done

    despositoryOptions, saleType = rightSideMenuObjs()
    try:
        bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
        bookValYear = bookValues.year
        # totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=bookValYear)
        totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=bookValYear)
        bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
    except:
        bookValues = bookValueCal = None

    try:
        fundingRoundsUnitInst = get_object_or_404(foundingRoundsFigureUnits, stockProfileName=stock)
    except:
        fundingRoundsUnitInst = None
    fundingRoundsUnitCreate = foundingRoundsFigureUnitsForm()

    try:
        fundingDetailsVisibilityInst = get_object_or_404(fundingDetailsVisibility, stockProfileName=stock)
    except:
        fundingDetailsVisibilityInst = None
    fundingDetailsVisibilityCreate = fundingDetailsVisibilityForm()

    currentStockPrice = localOrScreenerPriceView(stock)

    if essentialInst:
        totalSharesInst = essentialInst.totalShares
    else:
        totalSharesInst = 0

    try:
        stockProfitAndLossInst = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
        basicEps = stockProfitAndLossInst.basicEPS
        dilutedEps = stockProfitAndLossInst.dilutedEPS
    except:
        basicEps = 1
        dilutedEps = 1

    eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
    decimalEPS = return_decimal_or_0(eps)
    if decimalEPS == 0:
        decimalEPS = 1
    try:
        PEvalue = round((currentStockPrice / decimalEPS), 2)
    except:
        PEvalue = None

    if bookValues:
        bookVal = bookValueCal
    else:
        bookVal = 1
    try:
        PBvalue = round((currentStockPrice / bookVal), 2)
    except:
        PBvalue = None

    try:
        earningsYield = round((epsCY / currentStockPrice) * 100, 2)
    except:
        earningsYield = None

    try:
        dividendYield = round((dps / currentStockPrice) * 100, 2)
    except:
        dividendYield = None
    try:
        latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
        aumVals = latestBalanceSheet.aum
        aumGrowthVals = round(latestBalanceSheet.aumGrowth, 2)
    except:
        aumVals = None
        aumGrowthVals = None

    researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
    researchReportFAQsInstForm = researchReportFAQsForm()

    # Enterprise Value
    cashAndShortTermEqui = minorityInt = 0
    try:
        stockBalanceSheetLatestObj = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
        cashAndShortTermEqui = stockBalanceSheetLatestObj.cashAndCashEquivalents
        minorityInt = stockBalanceSheetLatestObj.minorityInterest

    except:
        pass
    balWithRBI = prefEquity = 0
    try:
        balWithRBI = essentialInst.balance_with_RBI
        prefEquity = essentialInst.preference_equity
    except:
        pass
    if not balWithRBI:
        balWithRBI = 0
    if not prefEquity:
        prefEquity = 0
    lgTermBorrow = curPortionOfLongTermDebt = srtTermBorrowings = leasLiability = 0
    try:
        latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
        if latestBalanceSheet.longTermBorrowings:
            lgTermBorrow = Decimal(latestBalanceSheet.longTermBorrowings)
        if latestBalanceSheet.currentPortionOfLongTermDebt:
            curPortionOfLongTermDebt = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
        if latestBalanceSheet.shortTermBorrowings:
            srtTermBorrowings = Decimal(latestBalanceSheet.shortTermBorrowings)
        if latestBalanceSheet.leaseLiability:
            leasLiability = Decimal(latestBalanceSheet.leaseLiability)
    except:
        pass
    totalDebt = lgTermBorrow + srtTermBorrowings + leasLiability + curPortionOfLongTermDebt
    try:
        marketCap = (totalSharesInst * currentStockPrice) / 10000000
    except:
        marketCap = None
    try:
        marketCapForEnterprise = numberConversion(marketCap, currentSystem='Cr',
                                                  convertTo=stock.stockProfileNameFFU.financialNumbers)
    except:
        marketCapForEnterprise = None
    enterpriseVal = returnDecimalOrZero(marketCapForEnterprise) - (
            returnDecimalOrZero(cashAndShortTermEqui) - returnDecimalOrZero(balWithRBI)) + returnDecimalOrZero(
        totalDebt) + returnDecimalOrZero(prefEquity) + returnDecimalOrZero(minorityInt)
    try:
        enterpriseVal = numberConversion(enterpriseVal, currentSystem=stock.stockProfileNameFFU.financialNumbers,
                                         convertTo='Cr')
    except:
        pass

    totalShareYearlyDataInst = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                   shareType='financial_year').order_by('year')
    totalShareYearlyDataInstConvertible = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                              shareType='convertible_equity').order_by(
        'year')
    totalShareYearlyDataInstForm = totalShareYearlyDataForm()
    commonFAQInstForm = commonFAQForm()
    commonFAQInst = commonFAQ.objects.all().order_by('id')
    researchReportFAQsInstForm = researchReportFAQsForm()

    try:
        newsVideosheadfinancial = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
            '-releasedDate')
    # print(newsVideosheadfinancial)
    except:
        newsVideosheadfinancial = []

    context = {
        'newsVideosheadfinancial': newsVideosheadfinancial,
        'bookValues': bookValues,
        'essentialInst': essentialInst,
        'createStockEssentials': createStockEssentials,
        'createStockEssentialsBottom': createStockEssentialsBottom,
        'stockInvestmentChecklistInst': stockInvestmentChecklistInst,
        'createstockInvestmentChecklist': createstockInvestmentChecklist,
        'stockIPOInst': stockIPOInst,
        'createStockIPO': createStockIPO,
        'stockDetailsInst': stockDetailsInst,
        'createStockDetails': createStockDetails,
        'createSubsidiariesBusModelStockDetails': createSubsidiariesBusModelStockDetails,
        'createProductStockDetails': createProductStockDetails,
        'createAssestStockDetails': createAssestStockDetails,
        'createIndustryOverviewStockDetails': createIndustryOverviewStockDetails,
        'stockFundingInst': stockFundingInst,
        'createStockFunding': createStockFunding,
        'stockFundingRoundsInst': stockFundingRoundsInst,
        'createStockFundingRounds': createStockFundingRounds,
        'promotorHolding': promotorHolding,
        'stockAdmInst': stockAdmInst,
        'createStockAdmin': createStockAdmin,
        'createStockAdminSnapshot': createStockAdminSnapshot,
        'createStockAbout': createStockAbout,
        'createawardsDescription': createawardsDescription,
        'createSSOTDescription': createSSOTDescription,
        'compoundSalesGrowth': revenueGrowth,
        'compoundProfitGrowth': compoundProfitGrowth,
        'totalRevCY': totalRevCY,
        'patCY': patCY,
        'epsCY': epsCY,
        'cashFlowOperationsCY': cashFlowOperationsCY,
        'cashFlowFinancingCY': cashFlowFinancingCY,
        'categoryForEss': categoryForEss,
        'sectorForEss': sectorForEss,
        'subSectorForEss': subSectorForEss,
        'returnedGrowthROEVal': returnedGrowthROEVal,
        'intrinsicVal': intrinsicVal,
        'revenueBreakupInst': revenueBreakupInst,
        'viewStockRevenueBreakUpForm': viewStockRevenueBreakUpForm,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'stock': stock,
        'fundingRoundsUnitInst': fundingRoundsUnitInst,
        'fundingRoundsUnitCreate': fundingRoundsUnitCreate,
        'fundingDetailsVisibilityInst': fundingDetailsVisibilityInst,
        'fundingDetailsVisibilityCreate': fundingDetailsVisibilityCreate,
        'benGrahamOrDCFInst': benGrahamOrDCFInst,
        'benGrahamOrDCFForm': benGrahamOrDCFCreate,
        'marketCap': marketCap,
        'PEvalue': PEvalue,
        'PBvalue': PBvalue,
        'earningsYield': earningsYield,
        'dividendYield': dividendYield,
        'bookValueCal': bookValueCal,
        'aumVals': aumVals,
        'aumGrowthVals': aumGrowthVals,
        'researchReportFAQsInst': researchReportFAQsInst,
        'researchReportFAQsInstForm': researchReportFAQsInstForm,
        'enterpriseVal': enterpriseVal,
        'totalShareYearlyDataInst': totalShareYearlyDataInst,
        'totalShareYearlyDataInstConvertible': totalShareYearlyDataInstConvertible,
        'totalShareYearlyDataInstForm': totalShareYearlyDataInstForm,
        'commonFAQInst': commonFAQInst,
        'commonFAQInstForm': commonFAQInstForm,
        'researchReportFAQsInstForm': researchReportFAQsInstForm,
    }

    return render(request, 'UI/snapshotForBankNBFCnew.html', context)


#
def keyRatioForBankNBFCsView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)

    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    stockProfitLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    balanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    cashFlow = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')[0:10]

    # Required changes in formuals Calculation starts - done

    deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgROceDenoPart = stockBalanceSheetCalculationForBankNBFc(
        stock)
    interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict = stockProfitAndLossCalculationForBankNBFc(
        stock)
    # Required changes in formuals Calculation ends - done

    returnOnEquity = {}
    roce = {}
    returnOnAssets = {}
    dividentYield = {}
    earningYield = {}
    for key, val in netIncomeDict.items():
        val2 = averageTotalEquityDict.get(key)
        if val2:
            valEquity = val2
        else:
            valEquity = 1

        catROERounded = round((val / valEquity) * 100, 2)
        returnOnEquity[key] = catROERounded
    for item in stockProfitLoss:
        # try:
        # 	currentStockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
        # 	currentStockPrice = currentStockPriceInst.investorPrice
        # except:
        # 	currentStockPrice = 0
        currentStockPrice = localOrScreenerPriceView(stock)
        # divident
        try:
            DPSforThisYear = item.DPS
        except:
            DPSforThisYear = None
        calDividentforThisYear = dividentYieldGraphView(DPSforThisYear, currentStockPrice)
        if calDividentforThisYear:
            dividentYield[item.year] = calDividentforThisYear
        # earning
        calEPSforThisYear = check_eps_basic_or_diluted(item.basicEPS, item.dilutedEPS)
        calEarningforThisYear = earningYieldGraphView(calEPSforThisYear, currentStockPrice)
        if calEarningforThisYear:
            earningYield[item.year] = calEarningforThisYear

    # Ishima remove ROCE  starts
    # for key, val in pbitDict.items():
    # 	val2 = avgTotalAssetDict.get(key)
    # 	val3 = avgROceDenoPart.get(key)
    # 	avgROceDenoPart
    # 	if val2:
    # 		valAverageAsset = val2
    # 	else :
    # 		valAverageAsset = 0

    # 	if val3:
    # 		valCurrentLiab = val3
    # 	else :
    # 		valCurrentLiab = 0

    # 	sumofAssestAndCrrLiabilities = valAverageAsset - valCurrentLiab
    # 	if not sumofAssestAndCrrLiabilities:
    # 		sumofAssestAndCrrLiabilities = 1
    # 	roce[key] = round((val / ( sumofAssestAndCrrLiabilities )) * 100,2)
    # Ishima aksed to remove ROCE ends

    for key, val in netIncomeDict.items():
        val2 = avgTotalAssetDict.get(key)
        # val3 = avgIntangibleAssetDict.get(key)
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0
        # if val3:
        # 	valAverageIntangibleAsset = val3
        # else :
        # 	valAverageIntangibleAsset = 0
        # processedVal = valAverageAsset - valAverageIntangibleAsset

        # changes from Kulmehar starts
        processedVal = valAverageAsset
        # chnages from Kulmehar ends

        if processedVal == 0:
            processedVal = 1

        returnOnAssets[key] = round((val / processedVal) * 100, 2)

    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None

    try:
        stockGrowthInst = stockGrowth.objects.get(stockProfileName=stock)
    except:
        stockGrowthInst = None
    createStockGrowth = stockGrowthForm(instance=stockGrowthInst)
    try:
        stockSolvencyInst = stockSolvency.objects.get(stockProfileName=stock)
    except:
        stockSolvencyInst = None
    createStockSolvency = stockSolvencyForm(instance=stockSolvencyInst)
    try:
        stockOperatingEfficiencyInst = stockOperatingEfficiency.objects.get(stockProfileName=stock)
    except:
        stockOperatingEfficiencyInst = None
    createStockOperatingEfficiency = stockOperatingEfficiencyForm(instance=stockOperatingEfficiencyInst)

    try:
        sectorSpecificRatiosInst = sectorSpecificRatios.objects.get(stockProfileName=stock)
    except:
        sectorSpecificRatiosInst = None
    createSectorSpecificRatios = sectorSpecificRatiosForm(instance=sectorSpecificRatiosInst)

    try:
        stockRatiosInst = stockRatios.objects.get(stockProfileName=stock)
    except:
        stockRatiosInst = None

    despositoryOptions, saleType = rightSideMenuObjs()
    createStockRatios = stockRatiosForm(instance=stockRatiosInst)

    # Required changes in formuals Calculation starts - done
    returnedGrowthDataRevenue, returnedRevenueGrowthAlgoProgrammedData, returnedNetProfitGrowthData, returnedNetProfitAlgoProgrammedData, returnedEPSGrowthData, returnedEPSAlgoProgrammedData, returnedEBITDAGrowthData, returnedEBITDAAlgoProgrammedData, returnedPBITGrowthData, returnedPBITAlgoProgrammedData = calGrowthTemplateDataViewFrBankNBFcs(
        stock)

    processedRevenueGrowthTextual = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    processedNetProfitGrowthTextual = calculateProgrammedGrowth(returnedNetProfitAlgoProgrammedData)
    processedEPSGrowthTextual = calculateProgrammedGrowth(returnedEPSAlgoProgrammedData)
    processedEBITDAGrowthTextual = calculateProgrammedGrowth(returnedEBITDAAlgoProgrammedData)
    processedPBITGrowthTextual = calculateProgrammedGrowth(returnedPBITAlgoProgrammedData)

    processedBookValueGrowthTextual = growthCalculatorForAnnualValuesFrBankNBFCs(stock, growthFor='bookValue')
    processedAssetGrowthTextual = growthCalculatorForAnnualValuesFrBankNBFCs(stock, growthFor='assetGrowth')
    processedCashFlowGrowthTextual, processedCashFlowGrowthFinancingTextual = growthCalculatorForAnnualValuesFrBankNBFCs(
        stock, growthFor='cashFlow')
    # Required changes in formuals Calculation ends - done

    indusSpecificGraphs = industrySpecificGraphs.objects.filter(stockProfileName=stock)
    industrySpecificGraph = industrySpecificGraphForm()

    industrySpecificValsGraph = industrySpecificGraphValsForm()
    indusGraphDict = {}
    for graph in indusSpecificGraphs:
        indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:10]
        indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by(
            '-year')[0:10]
        graphDict = {}
        dataDict = {}
        growthGraphDict = {}
        forCount = 0
        if graph.graphType == 'Value':
            graphDict['type'] = 'Value'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                forCount += 1
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
            for yearlyItemsGrowth in indusSpecificValsGraphsForGrowth:
                growthGraphDict[yearlyItemsGrowth.year] = yearlyItemsGrowth.value
            yearIs = 'key'
            requestFrom = 'keyRatioIndusSpecific'
            processedGrowthData = processDictForGrowthFormula(growthGraphDict, yearIs, requestFrom)
            growthData = calculateProgrammedGrowth(processedGrowthData)
            graphDict['growth'] = growthData
        else:
            graphDict['type'] = 'Percentage'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
        graphDict['data'] = dataDict
        graphDict['id'] = graph.id
        graphDict['description'] = graph.graphDescription
        graphDict['valueFori'] = graph.iDescription
        indusGraphDict[graph.graphFor] = graphDict
    processedDeRatio = sortingDictLowToHigh(deRatio)
    processedCurrentRatio = sortingDictLowToHigh(currentRatio)
    processedQuickRatio = sortingDictLowToHigh(quickRatio)
    bookValues = {}
    bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    for item in bookValuesObjs:
        try:
            totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=item.year)
            totalShareOutstanding = totalShareOutStandValueObj.totalCommonSharesOutstanding
            newBookValue = item.bookValue / totalShareOutstanding
            bookValues[item.year] = newBookValue
        except:
            pass

    bookValuestoEdit = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    createBookValue = bookValueDataForm()
    tier1CapitalRatioDict = {}
    tier2CapitalRatioDict = {}
    tangibleBookVaueDict = {}
    aumDict = {}
    aumGrowthDict = {}
    for item in balanceSheet:
        if item.tier1CapitalRatio:
            tier1CapitalRatioDict[item.year] = item.tier1CapitalRatio
        if item.tier2CapitalRatio:
            tier2CapitalRatioDict[item.year] = item.tier2CapitalRatio
        if item.tangibleBookValue:
            tangibleBookVaueDict[item.year] = item.tangibleBookValue
        if item.aum:
            aumDict[item.year] = item.aum
        if item.aumGrowth:
            aumGrowthDict[item.year] = item.aumGrowth

    #
    try:
        valuationRatioInst = valuationRatio.objects.latest('id')
    except:
        valuationRatioInst = None
    valuationRatioInstForm = valuationRatioForm(instance=valuationRatioInst)
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
    except:
        iDescriptionForKeyRatiosInst = None

    #
    try:
        # bankNBFCRatioDescriptionInst = bankNBFCRatioDescription.objects.latest('id')
        bankNBFCRatioDescriptionInst = bankNBFCRatioDescription.objects.get(stockProfileName=stock)
    except:
        bankNBFCRatioDescriptionInst = None
    bankNBFCRatioDescriptionInstForm = bankNBFCRatioDescriptionForm(instance=bankNBFCRatioDescriptionInst)
    RBIStandardVals = valuesRBIStandards.objects.all().order_by('year')
    companyForRBIVals = companyRatios.objects.filter(stockProfileName=stock).order_by('year')
    RBIGraphDict = {}
    commonRBIStockYearList = []
    for item in companyForRBIVals:
        if item.year:
            if RBIStandardVals.filter(year=item.year).exists():
                commonRBIStockYearList.append(item.year)
    tempDict = {}
    RBICompChart1 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart1 = True
        if RBIData.RBI_CARValue and stockData.carValue:
            tempList.append(RBIData.RBI_CARValue)
            tempList.append(stockData.carValue)
            tempDict[item] = tempList
    RBIGraphDict['CAR'] = tempDict
    tempDict = {}
    RBICompChart2 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart2 = True
        if RBIData.RBI_tier1Value and stockData.tier1Value:
            tempList.append(RBIData.RBI_tier1Value)
            tempList.append(stockData.tier1Value)
            tempDict[item] = tempList
    RBIGraphDict['tier1'] = tempDict
    tempDict = {}
    RBICompChart3 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart3 = True
        if RBIData.RBI_tier2Value and stockData.tier2Value:
            tempList.append(RBIData.RBI_tier2Value)
            tempList.append(stockData.tier2Value)
            tempDict[item] = tempList
    RBIGraphDict['tier2'] = tempDict
    tempDict = {}
    RBICompChart4 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart4 = True
        if RBIData.RBI_maintenanceMarginRequirement and stockData.maintenanceMarginRequirement:
            tempList.append(RBIData.RBI_maintenanceMarginRequirement)
            tempList.append(stockData.maintenanceMarginRequirement)
            tempDict[item] = tempList
    RBIGraphDict['MMR'] = tempDict
    companyRatioCreateForm = companyRatiosForm()

    try:
        regulatoryRatiosInst = regulatoryRatios.objects.get(stockProfileName=stock)
    except:
        regulatoryRatiosInst = None
    regulatoryRatiosInstForm = regulatoryRatiosForm(instance=regulatoryRatiosInst)

    try:
        newsVideosheadkeyratioBankNBFC = blogVideos.objects.filter(showinhead=True,
                                                                   relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadkeyratioBankNBFC = []

    try:
        typeofcompanyInstkeyratioBankNBFC = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstkeyratioBankNBFC = None

    context = {
        'stock': stock,
        'newsVideosheadkeyratioBankNBFC': newsVideosheadkeyratioBankNBFC,
        'typeofcompanyInstkeyratioBankNBFC': typeofcompanyInstkeyratioBankNBFC,
        'stockProfitLoss': stockProfitLoss,
        'stockBalanceSheet': balanceSheet,
        'cashFlow': cashFlow,
        'stockGrowthInst': stockGrowthInst,
        'createStockGrowth': createStockGrowth,
        'stockSolvencyInst': stockSolvencyInst,
        'createStockSolvency': createStockSolvency,
        'stockOperatingEfficiencyInst': stockOperatingEfficiencyInst,
        'createStockOperatingEfficiency': createStockOperatingEfficiency,
        'sectorSpecificRatiosInst': sectorSpecificRatiosInst,
        'createSectorSpecificRatios': createSectorSpecificRatios,
        'stockRatiosInst': stockRatiosInst,
        'createStockRatios': createStockRatios,
        'deRatio': processedDeRatio,
        'currentRatio': processedCurrentRatio,
        'quickRatio': processedQuickRatio,
        'interestCoverageRatio': interestCoverageRatio,
        'operatingProfitEBITmargin': operatingProfitEBITmargin,
        'pbtMargin': pbtMargin,
        'patMargin': patMargin,
        'returnOnEquity': returnOnEquity,
        'roce': roce,
        'returnOnAssets': returnOnAssets,
        'returnedGrowthDataRevenue': returnedGrowthDataRevenue,
        'returnedNetProfitGrowthData': returnedNetProfitGrowthData,
        'returnedEPSGrowthData': returnedEPSGrowthData,
        'returnedEBITDAGrowthData': returnedEBITDAGrowthData,
        'returnedPBITGrowthData': returnedPBITGrowthData,
        'processedRevenueGrowthTextual': processedRevenueGrowthTextual,
        'processedNetProfitGrowthTextual': processedNetProfitGrowthTextual,
        'processedEPSGrowthTextual': processedEPSGrowthTextual,
        'processedEBITDAGrowthTextual': processedEBITDAGrowthTextual,
        'processedPBITGrowthTextual': processedPBITGrowthTextual,
        'processedBookValueGrowthTextual': processedBookValueGrowthTextual,
        'processedAssetGrowthTextual': processedAssetGrowthTextual,
        'processedCashFlowGrowthTextual': processedCashFlowGrowthTextual,
        'processedCashFlowGrowthFinancingTextual': processedCashFlowGrowthFinancingTextual,
        'industrySpecificGraph': industrySpecificGraph,
        'industrySpecificValsGraph': industrySpecificValsGraph,
        'indusGraphDict': indusGraphDict,
        'createBookValue': createBookValue,
        'bookValues': bookValues,
        'stockAdmInst': stockAdmInst,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'bookValuestoEdit': bookValuestoEdit,
        'dividentYield': dividentYield,
        'earningYield': earningYield,
        'tier1CapitalRatio': tier1CapitalRatioDict,
        'tier2CapitalRatio': tier2CapitalRatioDict,
        'tangibleBookVaue': tangibleBookVaueDict,
        'aum': aumDict,
        'aumGrowth': aumGrowthDict,
        'valuationRatioInst': valuationRatioInst,
        'valuationRatioInstForm': valuationRatioInstForm,
        'iDescriptionForKeyRatiosInst': iDescriptionForKeyRatiosInst,
        'bankNBFCRatioDescriptionInst': bankNBFCRatioDescriptionInst,
        'bankNBFCRatioDescriptionInstForm': bankNBFCRatioDescriptionInstForm,
        'RBIGraphDict': RBIGraphDict,
        'companyForRBIVals': companyForRBIVals,
        'companyRatioCreateForm': companyRatioCreateForm,
        'regulatoryRatiosInst': regulatoryRatiosInst,
        'regulatoryRatiosInstForm': regulatoryRatiosInstForm,
        'RBICompChart1': RBICompChart1,
        'RBICompChart2': RBICompChart2,
        'RBICompChart3': RBICompChart3,
        'RBICompChart4': RBICompChart4,
    }
    return render(request, 'UI/keyRatioForBankNBFCs.html', context)


#
def financialForBankNBFCsView(request, slug):
    stock = get_object_or_404(stockBasicDetail, slug=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    includeFile = 'UI/financialProfitAndLossForBankNBFCs.html'
    activeNavTab = request.GET.get('nav')
    if activeNavTab:
        if activeNavTab == 'profit-and-loss':
            includeFile = 'UI/financialProfitAndLossForBankNBFCs.html'
        elif activeNavTab == 'cash-flow':
            includeFile = 'UI/financialCashFlow.html'
        elif activeNavTab == 'balance-sheet':
            includeFile = 'UI/financialBalanceSheetForBankNBFCs.html'
    fallBackFile = 'UI/financialProfitAndLossForBankNBFCs.html'
    tempToInclude = select_template([includeFile, fallBackFile])
    despositoryOptions, saleType = rightSideMenuObjs()

    financialStatementsFrProfitAndLossInst = financialStatementsFrProfitAndLoss.objects.filter(stockProfileName=stock)
    createFinancialStatementsFrProfitAndLoss = financialStatementsFrProfitAndLossForm()

    financialStatementsFrBalanceSheetInst = financialStatementsFrBalanceSheet.objects.filter(stockProfileName=stock)
    createFinancialStatementsFrBalanceSheet = financialStatementsFrBalanceSheetForm()

    financialStatementsFrCashFlowInst = financialStatementsFrCashFlow.objects.filter(stockProfileName=stock)
    createFinancialStatementsFrCashFlow = financialStatementsFrCashFlowForm()

    financialCompanyUpdatesInst = financialCompanyUpdates.objects.filter(stockProfileName=stock).order_by('title')
    createFinancialCompanyUpdates = financialCompanyUpdatesForm()

    stockProfitAndLossInst = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
    createstockProfitAndLoss = stockProfitAndLossBankNBFCForm()

    stockBalanceSheetInst = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
    createStockBalanceSheet = stockBalanceSheetBankNBFCForm()

    stockCashFlowInst = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')
    createStockCashFlow = stockCashFlowForm()
    try:
        figureUnitInst = get_object_or_404(financialFigureUnits, stockProfileName=stock)
    except:
        figureUnitInst = None
    financialFigureUnitsCreate = financialFigureUnitsForm()

    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
    except:
        stockAdmInst = None

    try:
        annualReportsDHRPInst = annualReportsDHRP.objects.get(stockProfileName=stock)
    except:
        annualReportsDHRPInst = None
    createAnnualReportsDHRP = annualReportsDHRPForm(instance=annualReportsDHRPInst)

    try:
        stockBalanceSheetBankNBFCTTMInst = stockBalanceSheetBankNBFCTTM.objects.get(stockProfileName=stock)
    except:
        stockBalanceSheetBankNBFCTTMInst = None
    createStockBalanceSheetBankNBFCTTM = stockBalanceSheetBankNBFCTTMForm(instance=stockBalanceSheetBankNBFCTTMInst)

    try:
        stockProfitAndLossBankNBFCTTMInst = stockProfitAndLossBankNBFCTTM.objects.get(stockProfileName=stock)
    except:
        stockProfitAndLossBankNBFCTTMInst = None
    createStockProfitAndLossBankNBFCTTM = stockProfitAndLossBankNBFCTTMForm(instance=stockProfitAndLossBankNBFCTTMInst)

    try:
        cashFlowTTMInst = stockCashFlowTTM.objects.get(stockProfileName=stock)
    except:
        cashFlowTTMInst = None
    createCashFlowTTM = stockCashFlowTTMForm(instance=cashFlowTTMInst)

    # description field for SEO - starts
    try:
        stockFinBalanceSheetSEOInst = stockFinBalanceSheetSEO.objects.get(stockProfileName=stock)
    except:
        stockFinBalanceSheetSEOInst = None
    createStockFinBalanceSheetSEO = stockFinBalanceSheetSEOForm(instance=stockFinBalanceSheetSEOInst)
    # description field for SEO - ends

    stockDeckAndDocsInst = stockDeckAndDocs.objects.filter(stockProfileName=stock).order_by('-id')
    stockDeckAndDocsInstForm = stockDeckAndDocsForm()

    try:
        newsVideosheadfinancialforbanknbfc = blogVideos.objects.filter(showinhead=True,
                                                                       relatedResearchReports=stock).order_by(
            '-releasedDate')
    except:
        newsVideosheadfinancialforbanknbfc = []

    try:
        typeofcompanyInstforbanknbfc = stockEssentials.objects.get(stockProfileName=stock)
    except:
        typeofcompanyInstforbanknbfc = None

    context = {
        'stock': stock,
        'includeFile': includeFile,
        'newsVideosheadfinancialforbanknbfc': newsVideosheadfinancialforbanknbfc,
        'typeofcompanyInstforbanknbfc': typeofcompanyInstforbanknbfc,
        'financialStatementsFrProfitAndLossInst': financialStatementsFrProfitAndLossInst,
        'createFinancialStatementsFrProfitAndLoss': createFinancialStatementsFrProfitAndLoss,
        'financialStatementsFrBalanceSheetInst': financialStatementsFrBalanceSheetInst,
        'createFinancialStatementsFrBalanceSheet': createFinancialStatementsFrBalanceSheet,
        'financialStatementsFrCashFlowInst': financialStatementsFrCashFlowInst,
        'createFinancialStatementsFrCashFlow': createFinancialStatementsFrCashFlow,
        'financialCompanyUpdatesInst': financialCompanyUpdatesInst,
        'createFinancialCompanyUpdates': createFinancialCompanyUpdates,
        'stockProfitAndLossInst': stockProfitAndLossInst,
        'createstockProfitAndLoss': createstockProfitAndLoss,
        'stockBalanceSheetInst': stockBalanceSheetInst,
        'createStockBalanceSheet': createStockBalanceSheet,
        'stockCashFlowInst': stockCashFlowInst,
        'createStockCashFlow': createStockCashFlow,
        'stockAdmInst': stockAdmInst,
        'figureUnitInst': figureUnitInst,
        'financialFigureUnitsCreate': financialFigureUnitsCreate,
        'despositoryOptions': despositoryOptions,
        'saleType': saleType,
        'annualReportsDHRPInst': annualReportsDHRPInst,
        'createAnnualReportsDHRP': createAnnualReportsDHRP,

        'cashFlowTTMInst': cashFlowTTMInst,
        'createCashFlowTTM': createCashFlowTTM,
        'stockFinBalanceSheetSEOInst': stockFinBalanceSheetSEOInst,
        'createStockFinBalanceSheetSEO': createStockFinBalanceSheetSEO,
        'stockBalanceSheetBankNBFCTTMInst': stockBalanceSheetBankNBFCTTMInst,
        'createStockBalanceSheetBankNBFCTTM': createStockBalanceSheetBankNBFCTTM,
        'stockProfitAndLossBankNBFCTTMInst': stockProfitAndLossBankNBFCTTMInst,
        'createStockProfitAndLossBankNBFCTTM': createStockProfitAndLossBankNBFCTTM,
        'stockDeckAndDocsInst': stockDeckAndDocsInst,
        'stockDeckAndDocsInstForm': stockDeckAndDocsInstForm,

    }

    return render(request, 'UI/financialForBankNBFCs.html', context)


#
def valuationRatioView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        parentProfile = request.POST.get('stockProfile')
        if parentProfile:
            parentProfileInst = get_object_or_404(stockBasicDetail, pk=parentProfile)
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(valuationRatio, pk=pkID)
        objForm = valuationRatioForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if parentProfileInst:
                cd.stockProfileName = parentProfileInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def iDescriptionForKeyRatiosView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        parentProfile = request.POST.get('stockProfile')
        if parentProfile:
            parentProfileInst = get_object_or_404(stockBasicDetail, pk=parentProfile)
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(valuationRatio, pk=pkID)
        objForm = iDescriptionForKeyRatiosForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if parentProfileInst:
                cd.stockProfileName = parentProfileInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def iDescriptionForKeyRatiosView(request, id=None):
    objInst = None
    redirectTo = 'stockApp:stockListURL'
    if id:
        objInst = get_object_or_404(currentRateOfbondYield, pk=id)
    if request.method == 'POST':
        currentRateForm = iDescriptionForKeyRatiosForm(request.POST, instance=objInst)
        if currentRateForm.is_valid():
            cd = currentRateForm.save(commit=False)
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'i Description for Key Ratio Graphs sent For Verification')
        else:
            messages.error(request, 'Wrong Input Data, Please check An Error occurred')
    return redirect(redirectTo)


#
def bankNBFCRatioDescriptionView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        parentProfile = request.POST.get('stockProfile')
        if parentProfile:
            parentProfileInst = get_object_or_404(stockBasicDetail, pk=parentProfile)
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(bankNBFCRatioDescription, pk=pkID)
        objForm = bankNBFCRatioDescriptionForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            if parentProfileInst:
                cd.stockProfileName = parentProfileInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def researchReportFAQsView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        parentProfile = request.POST.get('stockProfile')
        if parentProfile:
            parentProfileInst = get_object_or_404(stockBasicDetail, pk=parentProfile)
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(researchReportFAQs, pk=pkID)
        objForm = researchReportFAQsForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = parentProfileInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def totalShareYearlyDataView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        parentProfile = request.POST.get('stockProfile')
        if parentProfile:
            parentProfileInst = get_object_or_404(stockBasicDetail, pk=parentProfile)
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(totalShareYearlyData, pk=pkID)
        objForm = totalShareYearlyDataForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = parentProfileInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def valuesRBIStandardsSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        pkID = request.POST.get('dataID')
        objInst = None
        if methodType == 'update':
            objInst = get_object_or_404(valuesRBIStandards, pk=pkID)
        objForm = valuesRBIStandardsForm(request.POST, instance=objInst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect('stockApp:stockListURL')
    return HttpResponse('Invalid Entry')


#
def companyRatiosSubmitView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        parentProfile = request.POST.get('stockProfile')
        if parentProfile:
            parentProfileInst = get_object_or_404(stockBasicDetail, pk=parentProfile)
        if methodType == 'new':
            objlnst = None
            if companyRatios.objects.filter(stockProfileName=parentProfileInst, year=request.POST.get('year')).exists():
                messages.error(request, 'Value for this Year already Present, Try Editing perviously added value.')
                return redirect(redirectTo)
        else:
            objlnst = get_object_or_404(companyRatios, pk=pkID)
        objForm = companyRatiosForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = parentProfileInst
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def regulatoryRatiosView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(regulatoryRatios, stockProfileName=stockInst)
        objForm = regulatoryRatiosForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Regulatory Ratios sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
def stockPeersDescriptionForBankNBFCView(request):
    if request.method == 'POST':
        stockProfile = request.POST.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockPeersDescriptionForBankNBFC, stockProfileName=stockProfile)
        objForm = stockPeersDescriptionForBankNBFCForm(request.POST, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'stock Peers sent for verification')
        else:
            messages.error(request, objForm.errors)
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


@api_view(['POST'])
def stockPeersDescriptionForBankNBFCApiView(request):
    if request.method == 'POST' and request.user.is_staff:
        stockProfile = request.data.get('stockProfile')
        stockInst = get_object_or_404(stockBasicDetail, pk=stockProfile)
        methodType = request.data.get('submitType')
        redirectTo = request.data.get('requestFrom')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(stockPeersDescriptionForBankNBFC, stockProfileName=stockProfile)
        objForm = stockPeersDescriptionForBankNBFCForm(request.data, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.stockProfileName = stockInst
            if request.user.is_authenticated:
                cd.analyst = request.user
            try:
                cd.save()
                cd.refresh_from_db()
            except:
                return Response({'msg':'Description Data for this Stock is already Exists please pass "update" in submitType for update'})
            return Response({'msg':'stock Peers Description sent for verification'})
        else:
            return Response({'msg': objForm.errors})
    return Response({'msg':'Invalid Entry'})

#
def commonFAQView(request):
    if request.method == 'POST':
        methodType = request.POST.get('submitType')
        redirectTo = request.POST.get('requestFrom')
        pkID = request.POST.get('dataID')
        if methodType == 'new':
            objlnst = None
        else:
            objlnst = get_object_or_404(commonFAQ, pk=pkID)
        objForm = commonFAQForm(request.POST, request.FILES, instance=objlnst)
        if objForm.is_valid():
            cd = objForm.save(commit=False)
            cd.save()
            cd.refresh_from_db()
            messages.success(request, 'Data sent for verification')
        else:
            messages.error(request, 'Please check An Error occurred')
        return redirect(redirectTo)
    return HttpResponse('Invalid Entry')


#
@staff_member_required
def commonFAQRenderView(request):
    commonFAQInst = commonFAQ.objects.all().order_by('id')
    commonFAQInstForm = commonFAQForm()
    context = {
        'commonFAQInst': commonFAQInst,
        'commonFAQInstForm': commonFAQInstForm,
    }
    return render(request, 'staff-only/commonFAQs.html', context)


@api_view(['GET'])
def getKeyRatioView(request, slug):
    stock_detail = ""
    response_dict = {}
    stock = get_object_or_404(stockBasicDetail, id=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')
    renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
    if renderBankNBFCsTemplates:
        return redirect('stockApp:keyRatioForBankNBFCsApi', slug)
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    stockProfitLoss_list = []
    stockProfitLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if stockProfitLoss:
            for each in stockProfitLoss:
                stockProfitLoss_ser = stockProfitAndLossSerializer(each)
                stockProfitLoss_list.append(stockProfitLoss_ser.data)
    except:
        stockProfitLoss = None
        stockProfitLoss_list = []
    stockBalanceSheet_list = []
    balanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if balanceSheet:
            for each in balanceSheet:
                stockBalanceSheet_ser = stockBalanceSheetSerializer(each)
                stockBalanceSheet_list.append(stockBalanceSheet_ser.data)
    except:
        balanceSheet = None
        stockBalanceSheet_list = []
    stockCashFlow_list = []
    cashFlow = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if cashFlow:
            for each in cashFlow:
                stockCashFlow_ser = stockCashFlowSerializer(each)
                stockCashFlow_list.append(stockCashFlow_ser.data)
    except:
        cashFlow = None
        stockCashFlow_list = []
    deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgIntangibleAssetDict, avgROceDenoPart = stockBalanceSheetCalculation(
        stock)
    interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict = stockProfitAndLossCalculation(
        stock)
    returnOnEquity = {}
    roce = {}
    returnOnAssets = {}
    dividentYield = {}
    earningYield = {}
    for key, val in netIncomeDict.items():
        val2 = averageTotalEquityDict.get(key)
        if val2:
            valEquity = val2
        else:
            valEquity = 1
        catROERounded = round((val / valEquity) * 100, 2)
        returnOnEquity[key] = catROERounded
    for item in stockProfitLoss:
        currentStockPrice = localOrScreenerPriceView(stock)
        # try:
        #         currentStockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
        #         currentStockPrice = currentStockPriceInst.investorPrice
        # except:
        #         currentStockPrice = 0
        # divident
        try:
            DPSforThisYear = item.DPS
        except:
            DPSforThisYear = None
        calDividentforThisYear = dividentYieldGraphView(DPSforThisYear, currentStockPrice)
        if calDividentforThisYear:
            dividentYield[item.year] = calDividentforThisYear
        # earning
        calEPSforThisYear = check_eps_basic_or_diluted(item.basicEPS, item.dilutedEPS)
        calEarningforThisYear = earningYieldGraphView(calEPSforThisYear, currentStockPrice)
        if calEarningforThisYear:
            earningYield[item.year] = calEarningforThisYear
    # Ishima pointers changes for ROCE starts
    # for key, val in pbitDict.items():
    #         val2 = averageTotalEquityDict.get(key)
    #         val3 = avgROceDenoPart.get(key)
    #         avgROceDenoPart
    #         if val2:
    #                 valAverageEquity = val2
    #         else :
    #                 valAverageEquity = 0

    #         if val3:
    #                 valNonCurrentLiab = val3
    #         else :
    #                 valNonCurrentLiab = 0

    # sumofEquityAndNonCrrLiabilities = valAverageEquity + valNonCurrentLiab
    # if not sumofEquityAndNonCrrLiabilities:
    #         sumofEquityAndNonCrrLiabilities = 1
    # roce[key] = round((val / ( sumofEquityAndNonCrrLiabilities )) * 100,2)
    # Ishima pointers changes for ROCE ends
    for key, val in pbitDict.items():
        val2 = avgTotalAssetDict.get(key)
        val3 = avgROceDenoPart.get(key)
        avgROceDenoPart
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0

        if val3:
            valCurrentLiab = val3
        else:
            valCurrentLiab = 0

        sumofAssestAndCrrLiabilities = valAverageAsset - valCurrentLiab
        if not sumofAssestAndCrrLiabilities:
            sumofAssestAndCrrLiabilities = 1
        roce[key] = round((val / (sumofAssestAndCrrLiabilities)) * 100, 2)
    for key, val in netIncomeDict.items():
        val2 = avgTotalAssetDict.get(key)
        val3 = avgIntangibleAssetDict.get(key)
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0
        if val3:
            valAverageIntangibleAsset = val3
        else:
            valAverageIntangibleAsset = 0
        # processedVal = valAverageAsset - valAverageIntangibleAsset
        # changes from Kulmehar starts
        processedVal = valAverageAsset
        # chnages from Kulmehar ends
        if processedVal == 0:
            processedVal = 1
        returnOnAssets[key] = round((val / processedVal) * 100, 2)

    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
            stockAdmInst_detail = stockAdmInst_detail.data
        print("stockAdmInst", stockAdmInst)
    except:
        stockAdmInst = None
        stockAdmInst_detail = ""

    stockGrowthInst_detail = ""
    try:
        stockGrowthInst = stockGrowth.objects.get(stockProfileName=stock)
        if stockGrowthInst:
            stockGrowthInst_detail = stockGrowthSerializer(stockGrowthInst)
            stockGrowthInst_detail = stockGrowthInst_detail.data
        print("stockGrowthInst", stockGrowthInst)
    except:
        stockGrowthInst = None
        stockGrowthInst_detail = ""

    # createStockGrowth = stockGrowthForm(instance=stockGrowthInst)
    stockSolvencyInst_detail = ""
    try:
        stockSolvencyInst = stockSolvency.objects.get(stockProfileName=stock)
        if stockSolvencyInst:
            stockSolvencyInst_detail = stockSolvencySerializer(stockSolvencyInst)
            stockSolvencyInst_detail = stockSolvencyInst_detail.data
        print("stockSolvencyInst", stockSolvencyInst)
    except:
        stockSolvencyInst = None
        stockSolvencyInst_detail = ""
    # createStockSolvency = stockSolvencyForm(instance=stockSolvencyInst)
    stockOperatingEfficiencyInst_detail = ""
    try:
        stockOperatingEfficiencyInst = stockOperatingEfficiency.objects.get(stockProfileName=stock)
        if stockOperatingEfficiencyInst:
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencySerializer(stockOperatingEfficiencyInst)
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencyInst_detail.data
        print("stockOperatingEfficiencyInst", stockOperatingEfficiencyInst)
    except:
        stockOperatingEfficiencyInst = None
        stockOperatingEfficiencyInst_detail = ""
    # createStockOperatingEfficiency = stockOperatingEfficiencyForm(instance=stockOperatingEfficiencyInst)
    sectorSpecificRatiosInst_detail = ""
    try:
        sectorSpecificRatiosInst = sectorSpecificRatios.objects.get(stockProfileName=stock)
        if sectorSpecificRatiosInst:
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosSerializer(sectorSpecificRatiosInst)
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosInst_detail.data
        print('sectorSpecificRatiosInst', sectorSpecificRatiosInst)
    except:
        sectorSpecificRatiosInst = None
        sectorSpecificRatiosInst_detail = ""
    # createSectorSpecificRatios = sectorSpecificRatiosForm(instance=sectorSpecificRatiosInst)
    stockRatiosInst_detail = ""
    try:
        stockRatiosInst = stockRatios.objects.get(stockProfileName=stock)
        if stockRatiosInst:
            stockRatiosInst_detail = stockRatiosSerializer(stockRatiosInst)
            stockRatiosInst_detail = stockRatiosInst_detail.data
        print('stockRatiosInst', stockRatiosInst)
    except:
        stockRatiosInst = None
        stockRatiosInst_detail = ""
    despositoryOptions, saleType = rightSideMenuObjs()
    stockTransferDepositoryOptions_list = []
    try:
        if despositoryOptions:
            for each in despositoryOptions:
                stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
    except:
        despositoryOptions = None
        stockTransferDepositoryOptions_list = []
    saleTypeOptions_list = []
    try:
        if saleType:
            for each in saleType:
                saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                saleTypeOptions_list.append(saleTypeOptions_ser.data)
    except:
        saleType = None
        saleTypeOptions_list = []
    # createStockRatios = stockRatiosForm(instance=stockRatiosInst)
    returnedGrowthDataRevenue, returnedRevenueGrowthAlgoProgrammedData, returnedNetProfitGrowthData, returnedNetProfitAlgoProgrammedData, returnedEPSGrowthData, returnedEPSAlgoProgrammedData, returnedEBITDAGrowthData, returnedEBITDAAlgoProgrammedData, returnedPBITGrowthData, returnedPBITAlgoProgrammedData = calGrowthTemplateDataView(
        stock)
    processedRevenueGrowthTextual = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    processedNetProfitGrowthTextual = calculateProgrammedGrowth(returnedNetProfitAlgoProgrammedData)
    processedEPSGrowthTextual = calculateProgrammedGrowth(returnedEPSAlgoProgrammedData)
    processedEBITDAGrowthTextual = calculateProgrammedGrowth(returnedEBITDAAlgoProgrammedData)
    processedPBITGrowthTextual = calculateProgrammedGrowth(returnedPBITAlgoProgrammedData)
    processedBookValueGrowthTextual = growthCalculatorForAnnualValues(stock, growthFor='bookValue')
    processedAssetGrowthTextual = growthCalculatorForAnnualValues(stock, growthFor='assetGrowth')
    processedCashFlowGrowthTextual, processedCashFlowGrowthFinancingTextual = growthCalculatorForAnnualValues(stock,
                                                                                                              growthFor='cashFlow')
    indusSpecificGraphs = industrySpecificGraphs.objects.filter(stockProfileName=stock)
    industrySpecificGraph = industrySpecificGraphForm()
    industrySpecificValsGraph = industrySpecificGraphValsForm()
    indusGraphDict = {}
    for graph in indusSpecificGraphs:
        # indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:7]
        indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:10]
        # indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('-year')[0:7]
        indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by(
            '-year')[0:10]
        graphDict = {}
        dataDict = {}
        growthGraphDict = {}
        forCount = 0
        if graph.graphType == 'Value':
            graphDict['type'] = 'Value'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                forCount += 1
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
            for yearlyItemsGrowth in indusSpecificValsGraphsForGrowth:
                growthGraphDict[yearlyItemsGrowth.year] = yearlyItemsGrowth.value
            yearIs = 'key'
            requestFrom = 'keyRatioIndusSpecific'
            processedGrowthData = processDictForGrowthFormula(growthGraphDict, yearIs, requestFrom)
            growthData = calculateProgrammedGrowth(processedGrowthData)
            graphDict['growth'] = growthData
        else:
            graphDict['type'] = 'Percentage'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
        graphDict['data'] = dataDict
        graphDict['id'] = graph.id
        graphDict['description'] = graph.graphDescription
        indusGraphDict[graph.graphFor] = graphDict
    processedDeRatio = sortingDictLowToHigh(deRatio)
    processedCurrentRatio = sortingDictLowToHigh(currentRatio)
    processedQuickRatio = sortingDictLowToHigh(quickRatio)
    bookValues = {}
    bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    for item in bookValuesObjs:
        try:
            totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=item.year)
            totalShareOutstanding = totalShareOutStandValueObj.totalCommonSharesOutstanding
            newBookValue = item.bookValue / totalShareOutstanding
            bookValues[item.year] = newBookValue
        except:
            pass
    bookValuestoEdit = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    bookValuestoEdit_list = []
    try:
        if bookValuestoEdit:
            for each in bookValuestoEdit:
                bookValuestoEdit_ser = bookValueDataSerializer(each)
                bookValuestoEdit_list.append(bookValuestoEdit_ser.data)
    except:
        bookValuestoEdit = None
        bookValuestoEdit_list = []

    # createBookValue = bookValueDataForm()
    #
    try:
        valuationRatioInst = valuationRatio.objects.latest('id')
        if valuationRatioInst:
            valuationRatioInst_details = valuationRatioSerializer(valuationRatioInst)
            valuationRatioInst_details = valuationRatioInst_details.data
    except:
        valuationRatioInst = None
        valuationRatioInst_details = ""
    valuationRatioInstForm = valuationRatioForm(instance=valuationRatioInst)
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
        if iDescriptionForKeyRatiosInst:
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosSerializer(iDescriptionForKeyRatiosInst)
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosInst_details.data
    except:
        iDescriptionForKeyRatiosInst = None
        iDescriptionForKeyRatiosInst_details = ""

    response_dict.update({
        'stock': stock_detail,
        'stockProfitLoss': stockProfitLoss_list,
        'stockBalanceSheet': stockBalanceSheet_list,
        'cashFlow': stockCashFlow_list,
        'stockGrowthInst': stockGrowthInst_detail,
        # 'createStockGrowth' : createStockGrowth,
        'stockSolvencyInst': stockSolvencyInst_detail,
        # 'createStockSolvency' : createStockSolvency,
        'stockOperatingEfficiencyInst': stockOperatingEfficiencyInst_detail,
        # 'createStockOperatingEfficiency' : createStockOperatingEfficiency,
        'sectorSpecificRatiosInst': sectorSpecificRatiosInst_detail,
        # 'createSectorSpecificRatios' : createSectorSpecificRatios,
        'stockRatiosInst': stockRatiosInst_detail,
        # 'createStockRatios' : createStockRatios,
        'deRatio': processedDeRatio,
        'currentRatio': processedCurrentRatio,
        'quickRatio': processedQuickRatio,
        'interestCoverageRatio': interestCoverageRatio,
        'operatingProfitEBITmargin': operatingProfitEBITmargin,
        'pbtMargin': pbtMargin,
        'patMargin': patMargin,
        'returnOnEquity': returnOnEquity,
        'roce': roce,
        'returnOnAssets': returnOnAssets,
        'returnedGrowthDataRevenue': returnedGrowthDataRevenue,
        'returnedNetProfitGrowthData': returnedNetProfitGrowthData,
        'returnedEPSGrowthData': returnedEPSGrowthData,
        'returnedEBITDAGrowthData': returnedEBITDAGrowthData,
        'returnedPBITGrowthData': returnedPBITGrowthData,
        'processedRevenueGrowthTextual': processedRevenueGrowthTextual,
        'processedNetProfitGrowthTextual': processedNetProfitGrowthTextual,
        'processedEPSGrowthTextual': processedEPSGrowthTextual,
        'processedEBITDAGrowthTextual': processedEBITDAGrowthTextual,
        'processedPBITGrowthTextual': processedPBITGrowthTextual,
        'processedBookValueGrowthTextual': processedBookValueGrowthTextual,
        'processedAssetGrowthTextual': processedAssetGrowthTextual,
        'processedCashFlowGrowthTextual': processedCashFlowGrowthTextual,
        'processedCashFlowGrowthFinancingTextual': processedCashFlowGrowthFinancingTextual,
        # 'industrySpecificGraph':industrySpecificGraph,
        # 'industrySpecificValsGraph':industrySpecificValsGraph,
        'indusGraphDict': indusGraphDict,
        # 'createBookValue':createBookValue,
        'bookValues': bookValues,
        'stockAdmInst': stockAdmInst_detail,
        'despositoryOptions': stockTransferDepositoryOptions_list,
        'saleType': saleTypeOptions_list,
        'bookValuestoEdit': bookValuestoEdit_list,
        'dividentYield': dividentYield,
        'earningYield': earningYield,
        'valuationRatioInst': valuationRatioInst_details,
        # 'valuationRatioInstForm' : valuationRatioInstForm,
        'iDescriptionForKeyRatiosInst': iDescriptionForKeyRatiosInst_details,
    })
    return Response({'response': response_dict})


#
@api_view(['GET'])
def getKeyRatioForBankNBFCsView(request, slug):
    stock_detail = ""
    response_dict = {}
    stock = get_object_or_404(stockBasicDetail, id=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    stockProfitLoss_list = []
    stockProfitLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if stockProfitLoss:
            for each in stockProfitLoss:
                stockProfitLoss_ser = stockProfitAndLossBankNBFCSerializer(each)
                stockProfitLoss_list.append(stockProfitLoss_ser.data)
    except:
        stockProfitLoss = None
        stockProfitLoss_list = []

    stockBalanceSheet_list = []
    balanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if balanceSheet:
            for each in balanceSheet:
                stockBalanceSheet_ser = stockBalanceSheetBankNBFCSerializer(each)
                stockBalanceSheet_list.append(stockBalanceSheet_ser.data)
    except:
        balanceSheet = None
        stockBalanceSheet_list = []
    stockCashFlow_list = []
    cashFlow = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if cashFlow:
            for each in cashFlow:
                stockCashFlow_ser = stockCashFlowSerializer(each)
                stockCashFlow_list.append(stockCashFlow_ser.data)
    except:
        cashFlow = None
        stockCashFlow_list = []
    # Required changes in formuals Calculation starts - done
    deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgROceDenoPart = stockBalanceSheetCalculationForBankNBFc(
        stock)
    interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict = stockProfitAndLossCalculationForBankNBFc(
        stock)
    # Required changes in formuals Calculation ends - done
    returnOnEquity = {}
    roce = {}
    returnOnAssets = {}
    dividentYield = {}
    earningYield = {}
    for key, val in netIncomeDict.items():
        val2 = averageTotalEquityDict.get(key)
        if val2:
            valEquity = val2
        else:
            valEquity = 1
        catROERounded = round((val / valEquity) * 100, 2)
        returnOnEquity[key] = catROERounded
    for item in stockProfitLoss:
        # try:
        #         currentStockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
        #         currentStockPrice = currentStockPriceInst.investorPrice
        # except:
        #         currentStockPrice = 0
        currentStockPrice = localOrScreenerPriceView(stock)
        # divident
        try:
            DPSforThisYear = item.DPS
        except:
            DPSforThisYear = None
        calDividentforThisYear = dividentYieldGraphView(DPSforThisYear, currentStockPrice)
        if calDividentforThisYear:
            dividentYield[item.year] = calDividentforThisYear
        # earning
        calEPSforThisYear = check_eps_basic_or_diluted(item.basicEPS, item.dilutedEPS)
        calEarningforThisYear = earningYieldGraphView(calEPSforThisYear, currentStockPrice)
        if calEarningforThisYear:
            earningYield[item.year] = calEarningforThisYear
    # Ishima remove ROCE  starts
    # for key, val in pbitDict.items():
    #         val2 = avgTotalAssetDict.get(key)
    #         val3 = avgROceDenoPart.get(key)
    #         avgROceDenoPart
    #         if val2:
    #                 valAverageAsset = val2
    #         else :
    #                 valAverageAsset = 0

    #         if val3:
    #                 valCurrentLiab = val3
    #         else :
    #                 valCurrentLiab = 0

    #         sumofAssestAndCrrLiabilities = valAverageAsset - valCurrentLiab
    #         if not sumofAssestAndCrrLiabilities:
    #                 sumofAssestAndCrrLiabilities = 1
    #         roce[key] = round((val / ( sumofAssestAndCrrLiabilities )) * 100,2)
    # Ishima aksed to remove ROCE ends
    for key, val in netIncomeDict.items():
        val2 = avgTotalAssetDict.get(key)
        # val3 = avgIntangibleAssetDict.get(key)
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0
        # if val3:
        #         valAverageIntangibleAsset = val3
        # else :
        #         valAverageIntangibleAsset = 0
        # processedVal = valAverageAsset - valAverageIntangibleAsset
        # changes from Kulmehar starts
        processedVal = valAverageAsset
        # chnages from Kulmehar ends
        if processedVal == 0:
            processedVal = 1
        returnOnAssets[key] = round((val / processedVal) * 100, 2)

    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
            stockAdmInst_detail = stockAdmInst_detail.data
        print("stockAdmInst", stockAdmInst)
    except:
        stockAdmInst = None
        stockAdmInst_detail = ""

    stockGrowthInst_detail = ""
    try:
        stockGrowthInst = stockGrowth.objects.get(stockProfileName=stock)
        if stockGrowthInst:
            stockGrowthInst_detail = stockGrowthSerializer(stockGrowthInst)
            stockGrowthInst_detail = stockGrowthInst_detail.data
        print("stockGrowthInst", stockGrowthInst)
    except:
        stockGrowthInst = None
        stockGrowthInst_detail = ""
    # createStockGrowth = stockGrowthForm(instance=stockGrowthInst)
    stockSolvencyInst_detail = ""
    try:
        stockSolvencyInst = stockSolvency.objects.get(stockProfileName=stock)
        if stockSolvencyInst:
            stockSolvencyInst_detail = stockSolvencySerializer(stockSolvencyInst)
            stockSolvencyInst_detail = stockSolvencyInst_detail.data
        print("stockSolvencyInst", stockSolvencyInst)
    except:
        stockSolvencyInst = None
        stockSolvencyInst_detail = ""
    # createStockSolvency = stockSolvencyForm(instance=stockSolvencyInst)
    stockOperatingEfficiencyInst_detail = ""
    try:
        stockOperatingEfficiencyInst = stockOperatingEfficiency.objects.get(stockProfileName=stock)
        if stockOperatingEfficiencyInst:
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencySerializer(stockOperatingEfficiencyInst)
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencyInst_detail.data
        print("stockOperatingEfficiencyInst", stockOperatingEfficiencyInst)
    except:
        stockOperatingEfficiencyInst = None
        stockOperatingEfficiencyInst_detail = ""
    # createStockOperatingEfficiency = stockOperatingEfficiencyForm(instance=stockOperatingEfficiencyInst)
    sectorSpecificRatiosInst_detail = ""
    try:
        sectorSpecificRatiosInst = sectorSpecificRatios.objects.get(stockProfileName=stock)
        if sectorSpecificRatiosInst:
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosSerializer(sectorSpecificRatiosInst)
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosInst_detail.data
        print('sectorSpecificRatiosInst', sectorSpecificRatiosInst)
    except:
        sectorSpecificRatiosInst = None
        sectorSpecificRatiosInst_detail = ""
    # createSectorSpecificRatios = sectorSpecificRatiosForm(instance=sectorSpecificRatiosInst)
    stockRatiosInst_detail = ""
    try:
        stockRatiosInst = stockRatios.objects.get(stockProfileName=stock)
        if stockRatiosInst:
            stockRatiosInst_detail = stockRatiosSerializer(stockRatiosInst)
            stockRatiosInst_detail = stockRatiosInst_detail.data
        print('stockRatiosInst', stockRatiosInst)
    except:
        stockRatiosInst = None
        stockRatiosInst_detail = ""
    despositoryOptions, saleType = rightSideMenuObjs()
    # createStockRatios = stockRatiosForm(instance=stockRatiosInst)
    stockTransferDepositoryOptions_list = []
    try:
        if despositoryOptions:
            for each in despositoryOptions:
                stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
    except:
        despositoryOptions = None
        stockTransferDepositoryOptions_list = []
    saleTypeOptions_list = []
    try:
        if saleType:
            for each in saleType:
                saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                saleTypeOptions_list.append(saleTypeOptions_ser.data)
    except:
        saleType = None
        saleTypeOptions_list = []
    # Required changes in formuals Calculation starts - done
    returnedGrowthDataRevenue, returnedRevenueGrowthAlgoProgrammedData, returnedNetProfitGrowthData, returnedNetProfitAlgoProgrammedData, returnedEPSGrowthData, returnedEPSAlgoProgrammedData, returnedEBITDAGrowthData, returnedEBITDAAlgoProgrammedData, returnedPBITGrowthData, returnedPBITAlgoProgrammedData = calGrowthTemplateDataViewFrBankNBFcs(
        stock)

    processedRevenueGrowthTextual = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    processedNetProfitGrowthTextual = calculateProgrammedGrowth(returnedNetProfitAlgoProgrammedData)
    processedEPSGrowthTextual = calculateProgrammedGrowth(returnedEPSAlgoProgrammedData)
    processedEBITDAGrowthTextual = calculateProgrammedGrowth(returnedEBITDAAlgoProgrammedData)
    processedPBITGrowthTextual = calculateProgrammedGrowth(returnedPBITAlgoProgrammedData)

    processedBookValueGrowthTextual = growthCalculatorForAnnualValuesFrBankNBFCs(stock, growthFor='bookValue')
    processedAssetGrowthTextual = growthCalculatorForAnnualValuesFrBankNBFCs(stock, growthFor='assetGrowth')
    processedCashFlowGrowthTextual, processedCashFlowGrowthFinancingTextual = growthCalculatorForAnnualValuesFrBankNBFCs(
        stock, growthFor='cashFlow')
    # Required changes in formuals Calculation ends - done
    indusSpecificGraphs = industrySpecificGraphs.objects.filter(stockProfileName=stock)
    industrySpecificGraph = industrySpecificGraphForm()
    industrySpecificValsGraph = industrySpecificGraphValsForm()
    indusGraphDict = {}
    for graph in indusSpecificGraphs:
        indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:10]
        indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by(
            '-year')[0:10]
        graphDict = {}
        dataDict = {}
        growthGraphDict = {}
        forCount = 0
        if graph.graphType == 'Value':
            graphDict['type'] = 'Value'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                forCount += 1
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
            for yearlyItemsGrowth in indusSpecificValsGraphsForGrowth:
                growthGraphDict[yearlyItemsGrowth.year] = yearlyItemsGrowth.value
            yearIs = 'key'
            requestFrom = 'keyRatioIndusSpecific'
            processedGrowthData = processDictForGrowthFormula(growthGraphDict, yearIs, requestFrom)
            growthData = calculateProgrammedGrowth(processedGrowthData)
            graphDict['growth'] = growthData
        else:
            graphDict['type'] = 'Percentage'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
        graphDict['data'] = dataDict
        graphDict['id'] = graph.id
        graphDict['description'] = graph.graphDescription
        graphDict['valueFori'] = graph.iDescription
        indusGraphDict[graph.graphFor] = graphDict
    processedDeRatio = sortingDictLowToHigh(deRatio)
    processedCurrentRatio = sortingDictLowToHigh(currentRatio)
    processedQuickRatio = sortingDictLowToHigh(quickRatio)
    bookValues = {}
    bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    for item in bookValuesObjs:
        try:
            totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=item.year)
            totalShareOutstanding = totalShareOutStandValueObj.totalCommonSharesOutstanding
            newBookValue = item.bookValue / totalShareOutstanding
            bookValues[item.year] = newBookValue
        except:
            pass
    bookValuestoEdit = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    bookValuestoEdit_list = []
    try:
        if bookValuestoEdit:
            for each in bookValuestoEdit:
                bookValuestoEdit_ser = bookValueDataSerializer(each)
                bookValuestoEdit_list.append(bookValuestoEdit_ser.data)
    except:
        bookValuestoEdit = None
        bookValuestoEdit_list = []
    # createBookValue = bookValueDataForm()
    tier1CapitalRatioDict = {}
    tier2CapitalRatioDict = {}
    tangibleBookVaueDict = {}
    aumDict = {}
    aumGrowthDict = {}
    for item in balanceSheet:
        if item.tier1CapitalRatio:
            tier1CapitalRatioDict[item.year] = item.tier1CapitalRatio
        if item.tier2CapitalRatio:
            tier2CapitalRatioDict[item.year] = item.tier2CapitalRatio
        if item.tangibleBookValue:
            tangibleBookVaueDict[item.year] = item.tangibleBookValue
        if item.aum:
            aumDict[item.year] = item.aum
        if item.aumGrowth:
            aumGrowthDict[item.year] = item.aumGrowth
    #
    try:
        valuationRatioInst = valuationRatio.objects.latest('id')
        if valuationRatioInst:
            valuationRatioInst_details = valuationRatioSerializer(valuationRatioInst)
            valuationRatioInst_details = valuationRatioInst_details.data
    except:
        valuationRatioInst = None
        valuationRatioInst_details = ""
    # valuationRatioInstForm = valuationRatioForm(instance=valuationRatioInst)
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
        if iDescriptionForKeyRatiosInst:
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosSerializer(iDescriptionForKeyRatiosInst)
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosInst_details.data
    except:
        iDescriptionForKeyRatiosInst = None
        iDescriptionForKeyRatiosInst_details = ""
    #
    bankNBFCRatioDescriptionInst_detail = ""
    try:
        # bankNBFCRatioDescriptionInst = bankNBFCRatioDescription.objects.latest('id')
        bankNBFCRatioDescriptionInst = bankNBFCRatioDescription.objects.get(stockProfileName=stock)
        if bankNBFCRatioDescriptionInst:
            bankNBFCRatioDescriptionInst_detail = bankNBFCRatioDescriptionSerializer(bankNBFCRatioDescriptionInst)
            bankNBFCRatioDescriptionInst_detail = bankNBFCRatioDescriptionInst_detail.data
    except:
        bankNBFCRatioDescriptionInst = None
        bankNBFCRatioDescriptionInst_detail = ""
    # bankNBFCRatioDescriptionInstForm = bankNBFCRatioDescriptionForm(instance=bankNBFCRatioDescriptionInst)
    RBIStandardVals = valuesRBIStandards.objects.all().order_by('year')
    RBIStandardVals_list = []
    try:
        if RBIStandardVals:
            for each in RBIStandardVals:
                RBIStandardVals_ser = valuesRBIStandardsSerializer(each)
                RBIStandardVals_list.append(RBIStandardVals_ser.data)
    except:
        RBIStandardVals_list = []
    companyForRBIVals = companyRatios.objects.filter(stockProfileName=stock).order_by('year')
    companyForRBIVals_list = []
    try:
        if companyForRBIVals:
            for each in companyForRBIVals:
                companyForRBIVals_ser = companyRatiosSerializer(each)
                companyForRBIVals_list.append(companyForRBIVals_ser.data)
    except:
        companyForRBIVals_list = []
    RBIGraphDict = {}
    commonRBIStockYearList = []
    for item in companyForRBIVals:
        if item.year:
            if RBIStandardVals.filter(year=item.year).exists():
                commonRBIStockYearList.append(item.year)
    tempDict = {}
    RBICompChart1 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart1 = True
        if RBIData.RBI_CARValue and stockData.carValue:
            tempList.append(RBIData.RBI_CARValue)
            tempList.append(stockData.carValue)
            tempDict[item] = tempList
    RBIGraphDict['CAR'] = tempDict
    tempDict = {}
    RBICompChart2 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart2 = True
        if RBIData.RBI_tier1Value and stockData.tier1Value:
            tempList.append(RBIData.RBI_tier1Value)
            tempList.append(stockData.tier1Value)
            tempDict[item] = tempList
    RBIGraphDict['tier1'] = tempDict
    tempDict = {}
    RBICompChart3 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart3 = True
        if RBIData.RBI_tier2Value and stockData.tier2Value:
            tempList.append(RBIData.RBI_tier2Value)
            tempList.append(stockData.tier2Value)
            tempDict[item] = tempList
    RBIGraphDict['tier2'] = tempDict
    tempDict = {}
    RBICompChart4 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart4 = True
        if RBIData.RBI_maintenanceMarginRequirement and stockData.maintenanceMarginRequirement:
            tempList.append(RBIData.RBI_maintenanceMarginRequirement)
            tempList.append(stockData.maintenanceMarginRequirement)
            tempDict[item] = tempList
    RBIGraphDict['MMR'] = tempDict
    # companyRatioCreateForm = companyRatiosForm()
    regulatoryRatiosInst_detail = ""
    try:
        regulatoryRatiosInst = regulatoryRatios.objects.get(stockProfileName=stock)
        if regulatoryRatiosInst:
            regulatoryRatiosInst_detail = regulatoryRatiosSerializer(regulatoryRatiosInst)
            regulatoryRatiosInst_detail = regulatoryRatiosInst_detail.data
    except:
        regulatoryRatiosInst = None
        regulatoryRatiosInst_detail = ""
    # regulatoryRatiosInstForm = regulatoryRatiosForm(instance=regulatoryRatiosInst)

    response_dict.update({
        'stock': stock_detail,
        'stockProfitLoss': stockProfitLoss_list,
        'stockBalanceSheet': stockBalanceSheet_list,
        'cashFlow': stockCashFlow_list,
        'stockGrowthInst': stockGrowthInst_detail,
        # 'createStockGrowth' : createStockGrowth,
        'stockSolvencyInst': stockSolvencyInst_detail,
        # 'createStockSolvency' : createStockSolvency,
        'stockOperatingEfficiencyInst': stockOperatingEfficiencyInst_detail,
        # 'createStockOperatingEfficiency' : createStockOperatingEfficiency,
        'sectorSpecificRatiosInst': sectorSpecificRatiosInst_detail,
        # 'createSectorSpecificRatios' : createSectorSpecificRatios,
        
        'stockRatiosInst': stockRatiosInst_detail,
        # 'createStockRatios' : createStockRatios,
        'deRatio': processedDeRatio,
        'currentRatio': processedCurrentRatio,
        'quickRatio': processedQuickRatio,
        'interestCoverageRatio': interestCoverageRatio,
        'operatingProfitEBITmargin': operatingProfitEBITmargin,
        'pbtMargin': pbtMargin,
        'patMargin': patMargin,
        'returnOnEquity': returnOnEquity,
        'roce': roce,
        'returnOnAssets': returnOnAssets,
        'returnedGrowthDataRevenue': returnedGrowthDataRevenue,
        'returnedNetProfitGrowthData': returnedNetProfitGrowthData,
        'returnedEPSGrowthData': returnedEPSGrowthData,
        'returnedEBITDAGrowthData': returnedEBITDAGrowthData,
        'returnedPBITGrowthData': returnedPBITGrowthData,
        'processedRevenueGrowthTextual': processedRevenueGrowthTextual,
        'processedNetProfitGrowthTextual': processedNetProfitGrowthTextual,
        'processedEPSGrowthTextual': processedEPSGrowthTextual,
        'processedEBITDAGrowthTextual': processedEBITDAGrowthTextual,
        'processedPBITGrowthTextual': processedPBITGrowthTextual,
        'processedBookValueGrowthTextual': processedBookValueGrowthTextual,
        'processedAssetGrowthTextual': processedAssetGrowthTextual,
        'processedCashFlowGrowthTextual': processedCashFlowGrowthTextual,
        'processedCashFlowGrowthFinancingTextual': processedCashFlowGrowthFinancingTextual,
        # 'industrySpecificGraph':industrySpecificGraph,
        # 'industrySpecificValsGraph':industrySpecificValsGraph,
        'indusGraphDict': indusGraphDict,
        # 'createBookValue':createBookValue,
        'bookValues': bookValues,
        'stockAdmInst': stockAdmIns t_detail,
        'despositoryOptions': stockTransferDepositoryOptions_list,
        'saleType': saleTypeOptions_list,
        'bookValuestoEdit': bookValuestoEdit_list,
        'dividentYield': dividentYield,
        'earningYield': earningYield,
        'tier1CapitalRatio': tier1CapitalRatioDict,
        'tier2CapitalRatio': tier2CapitalRatioDict,
        'tangibleBookVaue': tangibleBookVaueDict,
        'aum': aumDict,
        'aumGrowth': aumGrowthDict,
        'valuationRatioInst': valuationRatioInst_details,
        # 'valuationRatioInstForm':valuationRatioInstForm,
        'iDescriptionForKeyRatiosInst': iDescriptionForKeyRatiosInst_details,
        'bankNBFCRatioDescriptionInst': bankNBFCRatioDescriptionInst_detail,
        # 'bankNBFCRatioDescriptionInstForm' : bankNBFCRatioDescriptionInstForm,
        'RBIGraphDict': RBIGraphDict,
        'companyForRBIVals': companyForRBIVals_list,
        # 'companyRatioCreateForm': companyRatioCreateForm,
        'regulatoryRatiosInst': regulatoryRatiosInst_detail,
        # 'regulatoryRatiosInstForm':regulatoryRatiosInstForm,
        'RBICompChart1': RBICompChart1,
        'RBICompChart2': RBICompChart2,
        'RBICompChart3': RBICompChart3,
        'RBICompChart4': RBICompChart4,
    })
    return Response({'response': response_dict})


#
@api_view(['GET'])
def getFinancialForBankNBFCsView(request, slug):
    response_dict = {}
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    includeFile = 'UI/financialProfitAndLossForBankNBFCs.html'
    activeNavTab = request.GET.get('nav')
    if activeNavTab:
        if activeNavTab == 'profit-and-loss':
            includeFile = 'UI/financialProfitAndLossForBankNBFCs.html'
        elif activeNavTab == 'cash-flow':
            includeFile = 'UI/financialCashFlow.html'
        elif activeNavTab == 'balance-sheet':
            includeFile = 'UI/financialBalanceSheetForBankNBFCs.html'
    fallBackFile = 'UI/financialProfitAndLossForBankNBFCs.html'
    tempToInclude = select_template([includeFile, fallBackFile])
    despositoryOptions, saleType = rightSideMenuObjs()

    stockTransferDepositoryOptions_list = []
    try:
        if despositoryOptions:
            for each in despositoryOptions:
                stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
    except:
        despositoryOptions = None
        stockTransferDepositoryOptions_list = []

    saleTypeOptions_list = []
    try:
        if saleType:
            for each in saleType:
                saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                saleTypeOptions_list.append(saleTypeOptions_ser.data)
    except:
        saleType = None
        saleTypeOptions_list = []

    financialStatementsFrProfitAndLossInst_list = []
    financialStatementsFrProfitAndLossInst = financialStatementsFrProfitAndLoss.objects.filter(stockProfileName=stock)
    if financialStatementsFrProfitAndLossInst:
        for each in financialStatementsFrProfitAndLossInst:
            financialStatementsFrProfitAndLossInst_ser = financialStatementsFrProfitAndLossSerializer(each)
            financialStatementsFrProfitAndLossInst_list.append(financialStatementsFrProfitAndLossInst_ser.data)

    # createFinancialStatementsFrProfitAndLoss = financialStatementsFrProfitAndLossForm()

    financialStatementsFrBalanceSheetInst_list = []
    financialStatementsFrBalanceSheetInst = financialStatementsFrBalanceSheet.objects.filter(stockProfileName=stock)
    if financialStatementsFrBalanceSheetInst:
        for each in financialStatementsFrBalanceSheetInst:
            financialStatementsFrBalanceSheetInst_ser = financialStatementsFrBalanceSheetSerializer(each)
            financialStatementsFrBalanceSheetInst_list.append(financialStatementsFrBalanceSheetInst_ser.data)
    # createFinancialStatementsFrBalanceSheet = financialStatementsFrBalanceSheetForm()

    financialStatementsFrCashFlowInst_list = []
    financialStatementsFrCashFlowInst = financialStatementsFrCashFlow.objects.filter(stockProfileName=stock)
    if financialStatementsFrCashFlowInst:
        for each in financialStatementsFrCashFlowInst:
            financialStatementsFrCashFlowInst_ser = financialStatementsFrCashFlowSerializer(each)
            financialStatementsFrCashFlowInst_list.append(financialStatementsFrCashFlowInst_ser.data)
    # createFinancialStatementsFrCashFlow = financialStatementsFrCashFlowForm()

    financialCompanyUpdatesInst_list = []
    financialCompanyUpdatesInst = financialCompanyUpdates.objects.filter(stockProfileName=stock).order_by('title')
    if financialCompanyUpdatesInst:
        for each in financialCompanyUpdatesInst:
            financialCompanyUpdatesInst_ser = financialStatementsFrCashFlowSerializer(each)
            financialCompanyUpdatesInst_list.append(financialCompanyUpdatesInst_ser.data)
    # createFinancialCompanyUpdates = financialCompanyUpdatesForm()

    stockProfitAndLossInst_list = []
    stockProfitAndLossInst = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
    if len(stockProfitAndLossInst):
        for each in stockProfitAndLossInst:
            stockProfitAndLossInst_ser = stockProfitAndLossBankNBFCSerializer(each)
            stockProfitAndLossInst_list.append(stockProfitAndLossInst_ser.data)

    # createstockProfitAndLoss = stockProfitAndLossBankNBFCForm()

    stockBalanceSheetInst_list = []
    stockBalanceSheetInst = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
    if stockBalanceSheetInst:
        for each in stockBalanceSheetInst:
            stockBalanceSheetInst_ser = stockBalanceSheetBankNBFCSerializer(each)
            stockBalanceSheetInst_list.append(stockBalanceSheetInst_ser.data)
    # createStockBalanceSheet = stockBalanceSheetBankNBFCForm()

    stockCashFlowInst_list = []
    stockCashFlowInst = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')
    if stockCashFlowInst:
        for each in stockCashFlowInst:
            stockCashFlowInst_ser = stockCashFlowSerializer(each)
            stockCashFlowInst_list.append(stockCashFlowInst_ser.data)

    # createStockCashFlow = stockCashFlowForm()
    figureUnitInst_detail = ""
    try:
        figureUnitInst = get_object_or_404(financialFigureUnits, stockProfileName=stock)
        if figureUnitInst:
            figureUnitInst_detail = financialFigureUnitsSerializer(figureUnitInst)
            figureUnitInst_detail = figureUnitInst_detail.data
    except:
        figureUnitInst = None
        figureUnitInst_detail = ""
    # financialFigureUnitsCreate = financialFigureUnitsForm()

    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
            stockAdmInst_detail = stockAdmInst_detail.data
    except:
        stockAdmInst = None
        stockAdmInst_detail = ""

    annualReportsDHRPInst_detail = ""
    try:
        annualReportsDHRPInst = annualReportsDHRP.objects.get(stockProfileName=stock)
        if annualReportsDHRPInst:
            annualReportsDHRPInst_detail = annualReportsDHRPSerializer(annualReportsDHRPInst)
            annualReportsDHRPInst_detail = annualReportsDHRPInst_detail.data
    except:
        annualReportsDHRPInst = None
        annualReportsDHRPInst_detail = ""
    # createAnnualReportsDHRP = annualReportsDHRPForm(instance=annualReportsDHRPInst)

    BalanceSheetBankNBFCTTMInst_detail = ""
    try:
        stockBalanceSheetBankNBFCTTMInst = stockBalanceSheetBankNBFCTTM.objects.get(stockProfileName=stock)
        if stockBalanceSheetBankNBFCTTMInst:
            BalanceSheetBankNBFCTTMInst_detail = stockBalanceSheetBankNBFCTTMSerializer(
                stockBalanceSheetBankNBFCTTMInst)
            BalanceSheetBankNBFCTTMInst_detail = BalanceSheetBankNBFCTTMInst_detail.data
    except:
        stockBalanceSheetBankNBFCTTMInst = None
        BalanceSheetBankNBFCTTMInst_detail = ""

    # createStockBalanceSheetBankNBFCTTM = stockBalanceSheetBankNBFCTTMForm(instance=stockBalanceSheetBankNBFCTTMInst)

    ProfitAndLossBankNBFCTTMInst_detail = ""
    try:
        stockProfitAndLossBankNBFCTTMInst = stockProfitAndLossBankNBFCTTM.objects.get(stockProfileName=stock)
        if stockProfitAndLossBankNBFCTTMInst:
            ProfitAndLossBankNBFCTTMInst_detail = stockProfitAndLossBankNBFCTTMSerializer(
                stockProfitAndLossBankNBFCTTMInst)
            ProfitAndLossBankNBFCTTMInst_detail = ProfitAndLossBankNBFCTTMInst_detail.data
    except:
        stockProfitAndLossBankNBFCTTMInst = None
        ProfitAndLossBankNBFCTTMInst_detail = ""

    # createStockProfitAndLossBankNBFCTTM = stockProfitAndLossBankNBFCTTMForm(instance=stockProfitAndLossBankNBFCTTMInst)

    cashFlowTTMInst_detail = ""
    try:
        cashFlowTTMInst = stockCashFlowTTM.objects.get(stockProfileName=stock)
        if cashFlowTTMInst:
            cashFlowTTMInst_detail = stockCashFlowTTMSerializer(cashFlowTTMInst)
            cashFlowTTMInst_detail = cashFlowTTMInst_detail.data
    except:
        cashFlowTTMInst = None
        cashFlowTTMInst_detail = ""
    # createCashFlowTTM = stockCashFlowTTMForm(instance=cashFlowTTMInst)

    # description field for SEO - starts
    stockFinBalanceSheetSEOInst_detail = ""
    try:
        stockFinBalanceSheetSEOInst = stockFinBalanceSheetSEO.objects.get(stockProfileName=stock)
        if stockFinBalanceSheetSEOInst:
            stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOSerializer(stockFinBalanceSheetSEOInst)
            stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOInst_detail.data
    except:
        stockFinBalanceSheetSEOInst = None
        stockFinBalanceSheetSEOInst_detail = ""
    # createStockFinBalanceSheetSEO = stockFinBalanceSheetSEOForm(instance=stockFinBalanceSheetSEOInst)
    # description field for SEO - ends

    stockDeckAndDocsInst_list = []
    stockDeckAndDocsInst = stockDeckAndDocs.objects.filter(stockProfileName=stock).order_by('-id')
    if stockDeckAndDocsInst:
        for each in stockDeckAndDocsInst:
            stockDeckAndDocsInst_ser = stockDeckAndDocsSerializer(each)
            stockDeckAndDocsInst_list.append(stockDeckAndDocsInst_ser.data)
    # stockDeckAndDocsInstForm = stockDeckAndDocsForm()

    response_dict.update({
        'stock': stock_detail,
        'includeFile': includeFile,
        'financialStatementsFrProfitAndLossInst': financialStatementsFrProfitAndLossInst_list,
        # 'createFinancialStatementsFrProfitAndLoss':createFinancialStatementsFrProfitAndLoss,
        'financialStatementsFrBalanceSheetInst': financialStatementsFrBalanceSheetInst_list,
        # 'createFinancialStatementsFrBalanceSheet':createFinancialStatementsFrBalanceSheet,
        'financialStatementsFrCashFlowInst': financialStatementsFrCashFlowInst_list,
        # 'createFinancialStatementsFrCashFlow':createFinancialStatementsFrCashFlow,
        'financialCompanyUpdatesInst': financialCompanyUpdatesInst_list,
        # 'createFinancialCompanyUpdates':createFinancialCompanyUpdates,
        'stockProfitAndLossInst': stockProfitAndLossInst_list,
        # 'createstockProfitAndLoss':createstockProfitAndLoss,
        'stockBalanceSheetInst': stockBalanceSheetInst_list,
        # 'createStockBalanceSheet':createStockBalanceSheet,
        'stockCashFlowInst': stockCashFlowInst_list,
        # 'createStockCashFlow':createStockCashFlow,
        'stockAdmInst': stockAdmInst_detail,
        'figureUnitInst': figureUnitInst_detail,
        # 'financialFigureUnitsCreate': financialFigureUnitsCreate,
        'despositoryOptions': stockTransferDepositoryOptions_list,
        'saleType': saleTypeOptions_list,
        'annualReportsDHRPInst': annualReportsDHRPInst_detail,
        # 'createAnnualReportsDHRP':createAnnualReportsDHRP,

        'cashFlowTTMInst': cashFlowTTMInst_detail,
        # 'createCashFlowTTM':createCashFlowTTM,
        'stockFinBalanceSheetSEOInst': stockFinBalanceSheetSEOInst_detail,
        # 'createStockFinBalanceSheetSEO':createStockFinBalanceSheetSEO,
        'stockBalanceSheetBankNBFCTTMInst': BalanceSheetBankNBFCTTMInst_detail,
        # 'createStockBalanceSheetBankNBFCTTM':createStockBalanceSheetBankNBFCTTM,
        'stockProfitAndLossBankNBFCTTMInst': ProfitAndLossBankNBFCTTMInst_detail,
        # 'createStockProfitAndLossBankNBFCTTM':createStockProfitAndLossBankNBFCTTM,
        'stockDeckAndDocsInst': stockDeckAndDocsInst_list,
        # 'stockDeckAndDocsInstForm':stockDeckAndDocsInstForm,

    })

    return Response({'response': response_dict})


@api_view(['GET'])
def getsnapshotview_01(request, slug):
    if request.method == 'GET':
        response_dict = {}
        stock = get_object_or_404(stockBasicDetail, id=slug)
        # stock_detail = ""
        stock_detail = {}
        if stock:
            stock_detail = StockSerializer(stock)
            stock_serialized = stock_detail = stock_detail.data

        if stock.status == 'draft' and not request.user.is_staff:
            return Response({'response': 'websiteApp:buypreIPOUrl'})

        renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
        if renderBankNBFCsTemplates:
            return redirect('stockApp:banknbfcViewapiNew', slug)

        currentPrice = localOrScreenerPriceView(stock)
        print("current price", currentPrice)
        callingFunction = 'snapshot'

        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                #	for each in stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
            print("stockAdmInst", stockAdmInst)
        except:
            stockAdmInst = None
        # stockAdmInst_list = []
        essentialInst_list = []
        essentialInst_detail = ""
        try:
            essentialInst = stockEssentials.objects.get(stockProfileName=stock)
            if essentialInst:
                #	for each in stockAdmInst:
                essentialInst_detail = stockEssentialsSerializer(essentialInst)
                essentialInst_detail = essentialInst_detail.data
        except:
            essentialInst = None
            essentialInst_list = None
            essentialInst_detail = ""

        # stock_detail['Essentials']['Face Value'] = essentialInst_detail.ISIN
        # stock_detail["stockProfileNameSE"] = essentialInst_detail
        financialFigureUnitsInst_detail = ""
        try:
            financialFigureUnitsInst = financialFigureUnits.objects.get(stockProfileName=stock)
            if financialFigureUnitsInst:
                financialFigureUnitsInst_detail = financialFigureUnitsSerializer(financialFigureUnitsInst)
                financialFigureUnitsInst_detail = financialFigureUnitsInst_detail.data
        except:
            financialFigureUnitsInst = None
            financialFigureUnitsInst_detail = ""

        stock_detail["stockProfileNameFFU"] = financialFigureUnitsInst_detail

        stockInvestmentChecklistInst_detail = ""
        try:
            stockInvestmentChecklistInst = stockInvestmentChecklist.objects.get(stockProfileName=stock)
            if stockInvestmentChecklistInst:
                #	for each in stockInvestmentChecklistInst:
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistSerializer(stockInvestmentChecklistInst)
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistInst_detail.data
        except:
            stockInvestmentChecklistInst_list = None

        stock_detail["stockProfileNameSIC"] = stockInvestmentChecklistInst_detail

        stockIPOInst_details = ""
        try:
            stockIPOInst = stockIPO.objects.get(stockProfileName=stock)
            if stockIPOInst:
                #	for each in stockIPOInst:
                stockIPOInst_details = stockIPOSerializer(stockIPOInst)
                stockIPOInst_details = stockIPOInst_details.data
        except:
            stockIPOInst = None

        stock_detail["stockProfileNameSI"] = stockIPOInst_details

        stockDetailsInst_details = ""
        try:
            stockDetailsInst = stockDetails.objects.get(stockProfileName=stock)
            if stockDetailsInst:
                #	for each in stockDetailsInst:
                stockDetailsInst_details = stockDetailsSerializer(stockDetailsInst)
                stockDetailsInst_details = stockDetailsInst_details.data
        except:
            stockDetailsInst = None

        stock_detail["stockProfileNameSD"] = stockDetailsInst_details

        stockFundingRoundsInst_list = []
        try:
            stockFundingRoundsInst = stockFundingRounds.objects.filter(stockProfileName=stock).order_by(
                '-dateOfInvestment')
            if stockFundingRoundsInst:
                for each in stockFundingRoundsInst:
                    stockFundingRoundsInst_ser = stockFundingRoundsSerializer(each)
                    stockFundingRoundsInst_list.append(stockFundingRoundsInst_ser.data)
        except:
            stockFundingInst = None

        stockFundingInst_detail = ""
        try:
            stockFundingInst = stockFunding.objects.get(stockProfileName=stock)
            if stockFundingInst:
                #	for each in stockFundingInst:
                stockFundingInst_detail = stockFundingSerializer(stockFundingInst)
                stockFundingInst_detail = stockFundingInst_detail.data
        except:
            stockFundingInst = None

        stock_detail['stockProfileNameSF'] = stockFundingInst_detail

        try:
            promotorHolding = stockOwnershipPattern.objects.get(stockProfileName=stock, year=currentYear)
            promotorHolding = promotorHolding.totalPromoterholdingValue
        except:
            promotorHolding = None
        try:
            latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
            totalRevCY = latestProfitAndLoss.totalRevenue
            patCY = latestProfitAndLoss.netIncome
            epsCY = latestProfitAndLoss.basicEPS
            dps = latestProfitAndLoss.DPS
        except:
            totalRevCY = None
            patCY = None
            epsCY = None
            dps = None

        try:
            latestCashFlow = stockCashFlow.objects.filter(stockProfileName=stock).latest('year')
            cashFlowOperationsCY = latestCashFlow.cashFromOperatingActivities
            cashFlowFinancingCY = latestCashFlow.cashFromFinancingActivities
        except:
            cashFlowOperationsCY = None
            cashFlowFinancingCY = None

        categoryForEss = categoryOptions.objects.all().order_by('name')
        categoryForEss_list = []
        if categoryForEss:
            for each in categoryForEss:
                categoryForEss = categoryOptionsSerializer(each)
                categoryForEss_list.append(categoryForEss.data)
        sectorForEss = sectorOptions.objects.all().order_by('name')
        sectorForEss_list = []
        if sectorForEss:
            for each in sectorForEss:
                categoryForEss = sectorOptionsSerializer(each)
                sectorForEss_list.append(categoryForEss.data)
        subSectorForEss = subSectorOptions.objects.all().order_by('name')
        subSectorForEss_list = []
        if subSectorForEss:
            for each in subSectorForEss:
                subSectorForEss = subSectorOptionsSerializer(each)
                subSectorForEss_list.append(subSectorForEss.data)
        revenueBreakupInst = stockRevenueBreakUp.objects.filter(stockProfileName=stock)
        revenueBreakupInst_list = []
        if revenueBreakupInst:
            for each in revenueBreakupInst:
                revenueBreakupInst_ser = stockRevenueBreakUpSerializer(each)
                revenueBreakupInst_list.append(revenueBreakupInst_ser.data)
        benGrahamOrDCFInst_detail = ""
        try:
            benGrahamOrDCFInst = benGrahamOrDCF.objects.get(stockProfileName=stock)
            if benGrahamOrDCFInst:
                #	for each in benGrahamOrDCFInst:
                benGrahamOrDCFInst_detail = benGrahamOrDCFSerializer(benGrahamOrDCFInst)
                benGrahamOrDCFInst_detail = benGrahamOrDCFInst_detail.data
        except:
            benGrahamOrDCFInst = None
        returnedGrowthROEVal = ROEgrowthCalculator(stock)
        response_dict.update({"returnedGrowthROEVal": returnedGrowthROEVal})
        # return returnedGrowthROEVal
        intrinsicVal = intrinsicFormula(stock)
        response_dict.update({"intrinsicVal": intrinsicVal})
        returnedRevenueGrowthAlgoProgrammedData, processedNetProfitGrowthTextual = calGrowthTemplateDataView(stock,
                                                                                                             requestFrom='snapshot')
        compoundSalesGrowth = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
        # compoundProfitGrowth = calculateProgrammedGrowth(processedNetProfitGrowthTextual)
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        stockTransferDepositoryOptions_list = []
        try:
            if despositoryOptions:
                for each in despositoryOptions:
                    stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                    stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
        except:
            despositoryOptions = None
            stockTransferDepositoryOptions_list = []
        saleTypeOptions_list = []
        try:
            if saleType:
                for each in saleType:
                    saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                    saleTypeOptions_list.append(saleTypeOptions_ser.data)
        except:
            saleType = None
            saleTypeOptions_list = []

        profitAndLossQuerySet = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('-year')
        revenueGrowth = calculateGrowthNew(profitAndLossQuerySet, 'revenue')
        compoundProfitGrowth = calculateGrowthNew(profitAndLossQuerySet, 'netIncome')
        try:
            bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
            bookValYear = bookValues.year
            totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=bookValYear)
            bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
        except:
            bookValues = bookValueCal = None
        fundingRoundsUnitInst_detail = ""
        try:
            fundingRoundsUnitInst = get_object_or_404(foundingRoundsFigureUnits, stockProfileName=stock)
            if fundingRoundsUnitInst:
                fundingRoundsUnitInst_detail = foundingRoundsFigureUnitsSerializer(fundingRoundsUnitInst)
                fundingRoundsUnitInst_detail = fundingRoundsUnitInst_detail.data
        except:
            fundingRoundsUnitInst = None
            fundingRoundsUnitInst_detail = ""

        fundingDetailsVisibilityInst_detail = ""
        try:
            fundingDetailsVisibilityInst = get_object_or_404(fundingDetailsVisibility, stockProfileName=stock)
            if fundingDetailsVisibilityInst:
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilitySerializer(fundingDetailsVisibilityInst)
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilityInst_detail.data
        except:
            fundingDetailsVisibilityInst = None
            fundingDetailsVisibilityInst_detail = ""

        stock_detail['stockProfileNameFDVI'] = fundingDetailsVisibilityInst_detail

        if essentialInst:
            totalSharesInst = essentialInst.totalShares
        else:
            totalSharesInst = 0

        try:
            stockProfitAndLossInst = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
            basicEps = stockProfitAndLossInst.basicEPS
            dilutedEps = stockProfitAndLossInst.dilutedEPS
        except:
            basicEps = 1
            dilutedEps = 1

        eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
        try:
            PEvalue = round((currentPrice / eps), 2)
        except:
            PEvalue = None

        if bookValues:
            bookVal = bookValueCal
        else:
            bookVal = 1
        try:
            PBvalue = round((currentPrice / bookVal), 2)
        except:
            PBvalue = None

        try:
            earningsYield = round((epsCY / currentPrice) * 100, 2)
        except:
            earningsYield = None

        try:
            dividendYield = round((dps / currentPrice) * 100, 2)
        except:
            dividendYield = None

        # enterprise value
        cashAndShortTermEqui = minorityInt = 0
        try:
            stockBalanceSheetLatestObj = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
            cashAndShortTermEqui = stockBalanceSheetLatestObj.cashAndShortTermInvestments
            minorityInt = stockBalanceSheetLatestObj.minorityInterest
        except:
            pass
        balWithRBI = prefEquity = 0
        try:
            balWithRBI = essentialInst.balance_with_RBI
            prefEquity = essentialInst.preference_equity
        except:
            pass

        if not balWithRBI:
            balWithRBI = 0
        if not prefEquity:
            prefEquity = 0
        totalLngDebt = currPortLngTermDebt = currPortionLeases = lngTermPortionOfLeases = 0
        try:
            latestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
            if latestBalanceSheet.totalLongTermDebt:
                totalLngDebt = Decimal(latestBalanceSheet.totalLongTermDebt)
            if latestBalanceSheet.currentPortionOfLongTermDebt:
                currPortLngTermDebt = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
            if latestBalanceSheet.currentPortionOfLeases:
                currPortionLeases = Decimal(latestBalanceSheet.currentPortionOfLeases)
            if latestBalanceSheet.longTermPortionOfLeases:
                lngTermPortionOfLeases = Decimal(latestBalanceSheet.longTermPortionOfLeases)
        except:
            pass
        totalDebt = totalLngDebt + currPortionLeases + lngTermPortionOfLeases + currPortLngTermDebt
        try:
            marketCap = (totalSharesInst * currentPrice) / 10000000
            marketCapForEnterprise = marketCap
        except:
            marketCap = None
            marketCapForEnterprise = None
        try:
            marketCapForEnterprise = numberConversion(marketCapForEnterprise, currentSystem='Cr',
                                                      convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        enterpriseVal = returnDecimalOrZero(marketCapForEnterprise) - (
                returnDecimalOrZero(cashAndShortTermEqui) - returnDecimalOrZero(balWithRBI)) + returnDecimalOrZero(
            totalDebt) + returnDecimalOrZero(prefEquity) + returnDecimalOrZero(minorityInt)
        try:
            enterpriseVal = numberConversion(enterpriseVal, currentSystem=stock.stockProfileNameFFU.financialNumbers,
                                             convertTo='Cr')
        except:
            pass

        researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
        researchReportFAQsInst_list = []
        if len(researchReportFAQsInst):
            for each in researchReportFAQsInst:
                researchReportFAQs_serial = researchReportFAQsSerializer(each)
                researchReportFAQsInst_list.append(researchReportFAQs_serial.data)

        totalShareYearlyDataInst = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                       shareType='financial_year').order_by('year')
        totalShareYearlyDataInst_list = []
        if len(totalShareYearlyDataInst):
            for each in totalShareYearlyDataInst:
                totalShareYearly_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInst_list.append(totalShareYearly_serial.data)

        totalShareYearlyDataInstConvertible = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                                  shareType='convertible_equity').order_by(
            'year')
        totalShareYearlyDataInstConvertible_list = []
        if len(totalShareYearlyDataInstConvertible):
            for each in totalShareYearlyDataInstConvertible:
                totalShareYearlyData_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInstConvertible_list.append(totalShareYearlyData_serial.data)

        commonFAQInst = commonFAQ.objects.all().order_by('id')
        commonFAQInst_list = []
        if len(commonFAQInst):
            for each in commonFAQInst:
                commonFAQInst_serial = commonFAQSerializer(each)
                commonFAQInst_list.append(commonFAQInst_serial.data)
        try:
            foundingRoundsFigureUnitsInst = foundingRoundsFigureUnits.objects.get(stockProfileName=stock)
        except:
            foundingRoundsFigureUnitsInst = None

        response_dict = {}
        stock_detail = {}
        stock_detail['data'] = {}
        if stock_serialized:
            saleType_list = []
            for each in stock_serialized['saleType']:
                try:
                    saleType_list.append(get_object_or_404(saleTypeOptions, id=each).name)
                except:
                    saleType_list.append(each)
            stock_detail['data']['saleType'] = saleType_list

        # stock_detail['data']['fo'] = foundingRoundsFigureUnitsInst_list
        if stockFundingInst_detail:
            stock_detail['data']['stage'] = stockFundingInst_detail['stage']
            stock_detail['data']['lookingFor'] = stockFundingInst_detail['lookingFor']
        else:
            stock_detail['data']['stage'] = None
            stock_detail['data']['lookingFor'] = None
        if financialFigureUnitsInst_detail and 'financialNumbers' in financialFigureUnitsInst_detail:
            stock_detail['data']['financialNumbers'] = financialFigureUnitsInst_detail['financialNumbers']
        if benGrahamOrDCFInst_detail:
            stock_detail['data']['benGrahamOrDCFInst'] = benGrahamOrDCFInst_detail

        if stock.content:
            stock_detail['SEOContent'] = stock.content
        if stock.seoTitle:
            stock_detail['seoTitle'] = stock.seoTitle
        if stockDetailsInst_details or stockDetailsInst_details != "" or stockDetailsInst_details != []:
            stock_detail["stockProfileNameSD"] = stockDetailsInst_details
        if fundingDetailsVisibilityInst_detail or fundingDetailsVisibilityInst_detail != "" or fundingDetailsVisibilityInst_detail != []:
            stock_detail['stockProfileNameFDVI'] = fundingDetailsVisibilityInst_detail

        stock_detail['essentials'] = {'label': 'Essentials', 'data': {}, 'child': {}}
        if "ISIN" in essentialInst_detail and essentialInst_detail["ISIN"] != "":
            stock_detail['essentials']['data']['ISIN'] = essentialInst_detail["ISIN"]
        if "faceValue" in essentialInst_detail and essentialInst_detail["faceValue"] != "":
            stock_detail['essentials']['data']['faceValue'] = essentialInst_detail["faceValue"]
        if "totalShares" in essentialInst_detail and essentialInst_detail["totalShares"] != "":
            stock_detail['essentials']['data']['totalShares'] = essentialInst_detail["totalShares"]
        if "essentialsDescription" in essentialInst_detail and essentialInst_detail["essentialsDescription"] != "":
            stock_detail['essentials']['data']['essentialsDescription'] = essentialInst_detail["essentialsDescription"]
        if totalRevCY:
            stock_detail['essentials']['data']['totalRevCY'] = totalRevCY
        if patCY:
            stock_detail['essentials']['data']['patCY'] = patCY
        if epsCY:
            stock_detail['essentials']['data']['epsCY'] = epsCY
        if PEvalue:
            stock_detail['essentials']['data']['PEvalue'] = PEvalue
        if PBvalue:
            stock_detail['essentials']['data']['PBvalue'] = PBvalue
        if marketCap:
            stock_detail['essentials']['data']['marketCap'] = marketCap
        if enterpriseVal:
            stock_detail['essentials']['data']['enterpriseVal'] = enterpriseVal
        if bookValueCal:
            stock_detail['essentials']['data']['bookValueCal'] = bookValueCal
        if intrinsicVal:
            stock_detail['essentials']['data']['intrinsicVal'] = intrinsicVal
        if dividendYield:
            stock_detail['essentials']['data']['dividendYield'] = dividendYield
        if earningsYield:
            stock_detail['essentials']['data']['earningsYield'] = earningsYield
        if promotorHolding:
            stock_detail['essentials']['data']['promotorHolding'] = promotorHolding

        if 'sector' in essentialInst_detail and essentialInst_detail['sector'] != "":
            try:
                stock_detail['essentials']['data']['sector'] = get_object_or_404(sectorOptions,
                                                                                 id=essentialInst_detail['sector']).name
            except:
                stock_detail['essentials']['data']['sector'] = essentialInst_detail['sector']
        if 'subSector' in essentialInst_detail and essentialInst_detail['subSector'] != "":
            try:
                stock_detail['essentials']['data']['subSector'] = get_object_or_404(subSectorOptions,
                                                                                    id=essentialInst_detail[
                                                                                        'subSector']).name
            except:
                stock_detail['essentials']['data']['subSector'] = essentialInst_detail['subSector']
        if 'category' in essentialInst_detail and essentialInst_detail['category'] != "":
            try:
                stock_detail['essentials']['data']['category'] = get_object_or_404(categoryOptions,
                                                                                   id=essentialInst_detail[
                                                                                       'category']).name
            except:
                stock_detail['essentials']['data']['category'] = essentialInst_detail['category']
        if cashFlowOperationsCY:
            stock_detail['essentials']['data']['cashFlowOperationsCY'] = cashFlowOperationsCY
        if cashFlowFinancingCY:
            stock_detail['essentials']['data']['cashFlowFinancingCY'] = cashFlowFinancingCY
        if 'salesGrowthRateOfXYear' in essentialInst_detail and essentialInst_detail['salesGrowthRateOfXYear'] != "":
            stock_detail['essentials']['data']['salesGrowthRateOfXYear'] = essentialInst_detail[
                'salesGrowthRateOfXYear']

        if stock_detail['essentials']['data'] == {} and stock_detail['essentials']['child'] == {}:
            stock_detail.pop('essentials')

        if totalShareYearlyDataInst_list and totalShareYearlyDataInst_list != [] and totalShareYearlyDataInstConvertible_list and totalShareYearlyDataInstConvertible_list != []:
            stock_detail['totalShareYearlyData'] = {'label': 'Total Share Yearly Data', 'data': {}, 'child': {}}
            totalShareYearlyData_list = []
            for item in totalShareYearlyDataInst_list:
                temp = {}
                temp['shareType'] = item['shareType']
                temp['year'] = item['year']
                temp['totalShares'] = item['totalShares']
                # temp['fundName'] = item['fundName']
                # temp['fundingAmount'] = item['fundingAmount']
                # temp['currencySymbol'] = get_object_or_404(currencySymbolOptions, id=item['currencySymbol']).uniqueCode
                # temp['fundingUnitNumbers'] = None
                totalShareYearlyData_list.append(temp)

            totalShareYearlyDataConvertible_list = []
            for item in totalShareYearlyDataInstConvertible_list:
                temp = {}
                temp['shareType'] = item['shareType']
                temp['year'] = item['year']
                temp['totalShares'] = item['totalShares']
                # temp['fundName'] = item['fundName']
                # temp['fundingAmount'] = item['fundingAmount']
                # temp['currencySymbol'] = get_object_or_404(currencySymbolOptions, id=item['currencySymbol']).uniqueCode
                # temp['fundingUnitNumbers'] = None
                totalShareYearlyDataConvertible_list.append(temp)
            # totalShareYearlyDataInstConvertible_list
            stock_detail['totalShareYearlyData']['data']['totalShareYearlyData'] = totalShareYearlyData_list
            stock_detail['totalShareYearlyData']['data'][
                'totalShareYearlyDataConvertible'] = totalShareYearlyDataConvertible_list

        stock_detail['growth'] = {'label': "Growth", 'data': {}, 'child': {}}
        if revenueGrowth and revenueGrowth != {}:
            stock_detail['growth']['data']['revenueGrowth'] = revenueGrowth
        if compoundSalesGrowth and compoundSalesGrowth != {}:
            stock_detail['growth']['data']['compoundSalesGrowth'] = compoundSalesGrowth
        if compoundProfitGrowth and compoundProfitGrowth != {}:
            stock_detail['growth']['data']['compoundProfitGrowth'] = compoundProfitGrowth
        if returnedGrowthROEVal and returnedGrowthROEVal != {}:
            stock_detail['growth']['data']['returnedGrowthROEVal'] = returnedGrowthROEVal

        if stock_detail['growth']['data'] == {} and stock_detail['growth']['child'] == {}:
            stock_detail.pop('growth')

        stock_detail['about'] = {'label': 'About', 'data': {}, 'child': {}}
        if stock_detail['about']['data'] == {} and stock_detail['about']['child'] == {}:
            stock_detail.pop('about')

        if stockIPOInst_details and stockIPOInst_details != {}:
            stock_detail['IPODetails'] = {'label': 'IPO Details', 'data': {'stockProfileNameSI': stockIPOInst_details},
                                          'child': {}}

        if stockFundingRoundsInst_list and stockFundingRoundsInst_list != []:
            stock_detail['funding'] = {'label': 'Funding', 'data': {}, 'child': {}}
            fundingRounds_list = []
            for item in stockFundingRoundsInst_list:
                temp = {}
                temp['fundingRound'] = item['fundingRound']
                temp['dateOfInvestment'] = item['dateOfInvestment']
                temp['date_available'] = item['date_available']
                temp['fundedBy'] = item['fundedBy']
                temp['fundName'] = item['fundName']
                temp['fundingAmount'] = item['fundingAmount']
                try:
                    temp['fundingUnitNumbers'] = foundingRoundsFigureUnitsInst.fundingUnitNumbers
                except:
                    temp['fundingUnitNumbers'] = None

                try:
                    temp['currencySymbol'] = get_object_or_404(currencySymbolOptions,
                                                               id=item['currencySymbol']).uniqueCode
                except:
                    temp['currencySymbol'] = item['currencySymbol']
                fundingRounds_list.append(temp)

            stock_detail['funding']['data']['fundingRounds'] = fundingRounds_list

        stock_detail['merger&Acquisition'] = {'label': 'Merger & Acquisition', 'data': {}, 'child': {}}
        if 'mergerDescription' in stockDetailsInst_details and stockDetailsInst_details['mergerDescription'] != "":
            stock_detail['merger&Acquisition']['data']['mergerDescription'] = stockDetailsInst_details[
                'mergerDescription']
        if 'aquistionsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'aquistionsDescription'] != "":
            stock_detail['merger&Acquisition']['data']['aquistionsDescription'] = stockDetailsInst_details[
                'aquistionsDescription']
        if 'investmentsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'investmentsDescription'] != "":
            stock_detail['merger&Acquisition']['data']['investmentsDescription'] = stockDetailsInst_details[
                'investmentsDescription']

        if stock_detail['merger&Acquisition']['data'] == {} and stock_detail['merger&Acquisition']['child'] == {}:
            stock_detail.pop('merger&Acquisition')

        stock_detail['subsidiaries'] = {'label': 'Subsidiaries', 'data': {}, 'child': {}}
        if 'subsidiaryDescription' in stockDetailsInst_details:
            stock_detail['subsidiaries']['data']['subsidiaryDescription'] = stockDetailsInst_details[
                'subsidiaryDescription']

        if stock_detail['subsidiaries']['data'] == {} and stock_detail['subsidiaries']['child'] == {}:
            stock_detail.pop('subsidiaries')

        stock_detail['businessModel'] = {'label': 'Business Model', 'data': {}, 'child': {}}
        if 'businessModelDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'businessModelDescription'] != "":
            stock_detail['businessModel']['data']['businessModelDescription'] = stockDetailsInst_details[
                'businessModelDescription']

        if stock_detail['businessModel']['data'] == {} and stock_detail['businessModel']['child'] == {}:
            stock_detail.pop('businessModel')

        if revenueBreakupInst_list and revenueBreakupInst_list != []:
            stock_detail['revenueSegmentation'] = {'label': 'Revenue Segmentation',
                                                   'data': {'revenueBreakupInst': revenueBreakupInst_list}, 'child': {}}

        stock_detail['product&Services'] = {'label': 'Product & Services', 'data': {}, 'child': {}}
        if 'productsAndServicesDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'productsAndServicesDescription'] != "":
            stock_detail['product&Services']['data']['ProductsAndServicesDescription'] = stockDetailsInst_details[
                'productsAndServicesDescription']

        if stock_detail['product&Services']['data'] == {} and stock_detail['product&Services']['child'] == {}:
            stock_detail.pop('product&Services')

        stock_detail['assets'] = {'label': 'Assets', 'data': {}, 'child': {}}
        if 'assestsDescription' in stockDetailsInst_details and stockDetailsInst_details['assestsDescription'] != "":
            stock_detail['assets']['data']['assestsDescription'] = stockDetailsInst_details['assestsDescription']

        if stock_detail['assets']['data'] == {} and stock_detail['assets']['child'] == {}:
            stock_detail.pop('assets')

        stock_detail['industryOverview'] = {'label': 'Industry Overview', 'data': {}, 'child': {}}
        if 'industryStatisticsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'industryStatisticsDescription'] != "":
            stock_detail['industryOverview']['child']['industryStatisticsDescription'] = {
                'label': 'Industry Statistics Description',
                'data': {'industryStatisticsDescription': stockDetailsInst_details['industryStatisticsDescription']},
                'child': {}}
        # stock_detail['industryOverview']['child']['industryStatisticsDescription']['data']['industryStatisticsDescription'] = stockDetailsInst_details['industryStatisticsDescription']
        if 'futureProspectsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'futureProspectsDescription'] != "":
            stock_detail['industryOverview']['child']['futureProspectsDescription'] = {
                'label': 'Future Prospects Description',
                'data': {'futureProspectsDescription': stockDetailsInst_details['futureProspectsDescription']},
                'child': {}}
        # stock_detail['industryOverview']['child']['futureProspectsDescription']['data']['futureProspectsDescription'] = stockDetailsInst_details['futureProspectsDescription']
        if 'governmentInitiativesDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'governmentInitiativesDescription'] != "":
            stock_detail['industryOverview']['child']['governmentInitiativesDescription'] = {
                'label': 'Government Initiatives Description', 'data': {
                    'governmentInitiativesDescription': stockDetailsInst_details['governmentInitiativesDescription']},
                'child': {}}
        # stock_detail['industryOverview']['child']['governmentInitiativesDescription']['data']['governmentInitiativesDescription'] = stockDetailsInst_details['governmentInitiativesDescription']
        if stock_detail['industryOverview']['data'] == {} and stock_detail['industryOverview']['child'] == {}:
            stock_detail.pop('industryOverview')

        stock_detail['awards&Achievements'] = {'label': 'Awards & Achievements', 'data': {}, 'child': {}}
        if 'awardsDescription' in stockDetailsInst_details and stockDetailsInst_details['awardsDescription'] != "":
            stock_detail['awards&Achievements']['data']['awardsDescription'] = stockDetailsInst_details[
                'awardsDescription']
        if stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail != "":
            stock_detail['awards&Achievements']['data']['stockProfileNameSIC'] = stockInvestmentChecklistInst_detail

        if stock_detail['awards&Achievements']['data'] == {} and stock_detail['awards&Achievements']['child'] == {}:
            stock_detail.pop('awards&Achievements')

        stock_detail['swot'] = {'label': 'SWOT', 'data': {}, 'child': {}}
        if 'strengthsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'strengthsDescription'] != "":
            stock_detail['swot']['child']['strengthsDescription'] = {'label': 'Strengths Description', 'data': {
                'strengthsDescription': stockDetailsInst_details['strengthsDescription']}, 'child': {}}
        # stock_detail['swot']['child']['strengthsDescription']['data']['strengthsDescription'] = stockDetailsInst_details['strengthsDescription']
        if 'shortcomingsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'shortcomingsDescription'] != "":
            stock_detail['swot']['child']['shortcomingsDescription'] = {'label': 'Shortcomings Description', 'data': {
                'shortcomingsDescription': stockDetailsInst_details['shortcomingsDescription']}, 'child': {}}
        # stock_detail['swot']['child']['shortcomingsDescription']['data']['shortcomingsDescription'] = stockDetailsInst_details['shortcomingsDescription']
        if 'opportunitiesDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'opportunitiesDescription'] != "":
            stock_detail['swot']['child']['opportunitiesDescription'] = {'label': 'Opportunities Description', 'data': {
                'opportunitiesDescription': stockDetailsInst_details['opportunitiesDescription']}, 'child': {}}
        # stock_detail['swot']['child']['opportunitiesDescription']['data']['opportunitiesDescription'] = stockDetailsInst_details['opportunitiesDescription']
        if 'threatsDescription' in stockDetailsInst_details and stockDetailsInst_details['threatsDescription'] != "":
            stock_detail['swot']['child']['threatsDescription'] = {'label': 'Threats Description', 'data': {
                'threatsDescription': stockDetailsInst_details['threatsDescription']}, 'child': {}}
        # stock_detail['swot']['child']['threatsDescription']['data']['threatsDescription'] = stockDetailsInst_details['threatsDescription']

        if stock_detail['swot']['data'] == {} and stock_detail['swot']['child'] == {}:
            stock_detail.pop('swot')

        stock_detail['investmentChecklist'] = {'label': 'Investment Checklist', 'data': {}, 'child': {}}
        if 'management' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'management'] != "":
            stock_detail['investmentChecklist']['data']['management'] = stockInvestmentChecklistInst_detail[
                'management']
        if 'acountingPratice' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'acountingPratice'] != "":
            stock_detail['investmentChecklist']['data']['acountingPratice'] = stockInvestmentChecklistInst_detail[
                'acountingPratice']
        if 'profitability' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'profitability'] != "":
            stock_detail['investmentChecklist']['data']['profitability'] = stockInvestmentChecklistInst_detail[
                'profitability']
        if 'solvency' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail['solvency'] != "":
            stock_detail['investmentChecklist']['data']['solvency'] = stockInvestmentChecklistInst_detail['solvency']
        if 'growth' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail['growth'] != "":
            stock_detail['investmentChecklist']['data']['growth'] = stockInvestmentChecklistInst_detail['growth']
        if 'valuation' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'valuation'] != "":
            stock_detail['investmentChecklist']['data']['valuation'] = stockInvestmentChecklistInst_detail['valuation']
        if 'businessType' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'businessType'] != "":
            try:
                stock_detail['investmentChecklist']['data']['businessType'] = get_object_or_404(businessTypeOptions, id=
                stockInvestmentChecklistInst_detail['businessType']).name
            except:
                stock_detail['investmentChecklist']['data']['businessType'] = stockInvestmentChecklistInst_detail[
                    'businessType']
        if 'rating' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail['rating'] != "":
            stock_detail['investmentChecklist']['data']['rating'] = stockInvestmentChecklistInst_detail['rating']
        if 'recommendation' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'recommendation'] != "":
            try:
                stock_detail['investmentChecklist']['data']['recommendation'] = get_object_or_404(recommendationOptions,
                                                                                                  id=
                                                                                                  stockInvestmentChecklistInst_detail[
                                                                                                      'recommendation']).name
            except:
                stock_detail['investmentChecklist']['data']['recommendation'] = stockInvestmentChecklistInst_detail[
                    'recommendation']
        if 'accumulationRangeDescriptionFrom' in stockInvestmentChecklistInst_detail and \
                stockInvestmentChecklistInst_detail['accumulationRangeDescriptionFrom'] != "":
            stock_detail['investmentChecklist']['data']['accumulationRangeDescriptionFrom'] = \
            stockInvestmentChecklistInst_detail['accumulationRangeDescriptionFrom']
        if 'accumulationRangeDescriptionTo' in stockInvestmentChecklistInst_detail and \
                stockInvestmentChecklistInst_detail['accumulationRangeDescriptionTo'] != "":
            stock_detail['investmentChecklist']['data']['accumulationRangeDescriptionTo'] = \
            stockInvestmentChecklistInst_detail['accumulationRangeDescriptionTo']

        if stock_detail['investmentChecklist']['data'] == {} and stock_detail['investmentChecklist']['child'] == {}:
            stock_detail.pop('investmentChecklist')

        stock_detail['detailInfo'] = {'label': 'Detail Info', 'data': {}, 'child': {}}
        if 'typeOfCompany' in essentialInst_detail and essentialInst_detail['typeOfCompany'] != "":
            try:
                stock_detail['detailInfo']['data']['typeOfCompany'] = get_object_or_404(typeOfCompanyOptions,
                                                                                        id=essentialInst_detail[
                                                                                            'typeOfCompany']).name
            except:
                stock_detail['detailInfo']['data']['typeOfCompany'] = essentialInst_detail['typeOfCompany']
        if 'countryRegisteredIn' in essentialInst_detail and essentialInst_detail['countryRegisteredIn'] != "":
            try:
                stock_detail['detailInfo']['data']['countryRegisteredIn'] = get_object_or_404(countryOptions,
                                                                                              id=essentialInst_detail[
                                                                                                  'countryRegisteredIn']).name
            except:
                stock_detail['detailInfo']['data']['countryRegisteredIn'] = essentialInst_detail['countryRegisteredIn']
        if 'registeredDate' in essentialInst_detail and essentialInst_detail['registeredDate'] != "":
            stock_detail['detailInfo']['data']['registeredDate'] = essentialInst_detail['registeredDate']
        if 'researchLastUpdatedOn' in essentialInst_detail and essentialInst_detail['researchLastUpdatedOn'] != "":
            stock_detail['detailInfo']['data']['researchLastUpdatedOn'] = essentialInst_detail['researchLastUpdatedOn']
        if 'listingDate' in essentialInst_detail and essentialInst_detail['listingDate'] != "":
            stock_detail['detailInfo']['data']['listingDate'] = essentialInst_detail['listingDate']
        if 'stockExchangeReferenceSymbol' in essentialInst_detail and essentialInst_detail[
            'stockExchangeReferenceSymbol'] != "":
            stock_detail['detailInfo']['data']['stockExchangeReferenceSymbol'] = essentialInst_detail[
                'stockExchangeReferenceSymbol']
        if 'regOffice' in essentialInst_detail and essentialInst_detail['regOffice'] != "":
            stock_detail['detailInfo']['data']['regOffice'] = essentialInst_detail['regOffice']
        if 'website' in essentialInst_detail and essentialInst_detail['website'] != "":
            stock_detail['detailInfo']['data']['website'] = essentialInst_detail['website']

        if stock_detail['detailInfo']['data'] == {} and stock_detail['detailInfo']['child'] == {}:
            stock_detail.pop('detailInfo')

        response_dict.update({"stock": stock_detail})

        # print(response_dict['detailInfo']['data']['website'])

        # response_dict.update({#"essentialInst": essentialInst_detail,
        #					"stock": stock_detail,
        #					"stockFundingRoundsInst": stockFundingRoundsInst_list,
        #					  "returnedRevenueGrowthAlgoProgrammedData": returnedRevenueGrowthAlgoProgrammedData,
        #					  "processedNetProfitGrowthTextual": processedNetProfitGrowthTextual,
        #					  "compoundSalesGrowth": compoundSalesGrowth,
        #					  "despositoryOptions": despositoryOptions,
        #					  "saleType": saleType,
        #					  "revenueGrowth": revenueGrowth,
        #					  "compoundProfitGrowth": compoundProfitGrowth,
        #					  "fundingRoundsUnitInst": fundingRoundsUnitInst_detail,
        #					  "enterpriseVal": enterpriseVal,
        #					  "PEvalue": PEvalue,
        #					  "PBvalue": PBvalue,
        #					  "earningsYield": earningsYield,
        #					  "dividendYield": dividendYield,
        #					  "researchReportFAQsInst": researchReportFAQsInst_list,
        #					  "totalShareYearlyDataInst": totalShareYearlyDataInst_list,
        #					  "totalShareYearlyDataInstConvertible": totalShareYearlyDataInstConvertible_list,
        #					  "commonFAQInst": commonFAQInst_list,
        #					  "cashFlowOperationsCY": cashFlowOperationsCY,
        #					  "cashFlowFinancingCY": cashFlowFinancingCY,
        #					  "promotorHolding": promotorHolding,
        #					  "totalRevCY": totalRevCY,
        #					  "patCY": patCY,
        #					  "marketCap": marketCap,
        #					  "stockAdmInst": stockAdmInst_detail,
        #					  #"stockInvestmentChecklistInst": stockInvestmentChecklistInst_list,
        #					  "categoryForEss": categoryForEss_list,
        #					  "sectorForEss": sectorForEss_list,
        #					  "subSectorForEss": subSectorForEss_list,
        # "stockIPOInst": stockIPOInst_list,
        # "stockDetailsInst": stockDetailsInst_list,
        #					  "epsCY": epsCY,
        #					  "returnedGrowthROEVal": returnedGrowthROEVal,
        #					  "intrinsicVal":intrinsicVal,
        #					  "benGrahamOrDCFInst": benGrahamOrDCFInst_detail,
        #					  "revenueBreakupInst": revenueBreakupInst_list})
        return Response({'response': response_dict})


@api_view(['GET'])
def snapshotForBankNBFCsViewAPI_01(request, slug):
    print(slug)
    if request.method == 'GET':
        print("yaha aaya")
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = ""
        if stock:
            stock_detail = StockSerializer(stock)
            stock_serialized = stock_detail = stock_detail.data
        if stock.status == 'draft' and not request.user.is_staff:
            return redirect('websiteApp:buypreIPOUrl')

        callingFunction = 'snapshot'
        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
        except:
            stockAdmInst = None
        # createStockAdmin = stockAdminForm(instance=stockAdmInst)
        # createStockAdminSnapshot = stockAdminSnapshotForm(instance=stockAdmInst)

        benGrahamOrDCFInst_detail = ""
        try:
            benGrahamOrDCFInst = benGrahamOrDCF.objects.get(stockProfileName=stock)
            if benGrahamOrDCFInst:
                #   for each in benGrahamOrDCFInst:
                benGrahamOrDCFInst_detail = benGrahamOrDCFSerializer(benGrahamOrDCFInst)
                benGrahamOrDCFInst_detail = benGrahamOrDCFInst_detail.data
        except:
            benGrahamOrDCFInst = None
        # benGrahamOrDCFCreate = benGrahamOrDCFForm(instance=benGrahamOrDCFInst)

        essentialInst_list = []
        essentialInst_detail = ""
        try:
            essentialInst = stockEssentials.objects.get(stockProfileName=stock)
            if essentialInst:
                #   for each in stockAdmInst:
                essentialInst_detail = stockEssentialsSerializer(essentialInst)
                essentialInst_detail = essentialInst_detail.data
        except:
            essentialInst = None
            essentialInst_list = None
            essentialInst_detail = ""
        stock_detail["stockProfileNameSE"] = essentialInst_detail
        financialFigureUnitsInst_detail = ""
        try:
            financialFigureUnitsInst = financialFigureUnits.objects.get(stockProfileName=stock)
            if financialFigureUnitsInst:
                financialFigureUnitsInst_detail = financialFigureUnitsSerializer(financialFigureUnitsInst)
                financialFigureUnitsInst_detail = financialFigureUnitsInst_detail.data
        except:
            financialFigureUnitsInst = None
            financialFigureUnitsInst_detail = ""

        stock_detail["stockProfileNameFFU"] = financialFigureUnitsInst_detail

        stockInvestmentChecklistInst_detail = ""
        try:
            stockInvestmentChecklistInst = stockInvestmentChecklist.objects.get(stockProfileName=stock)
            if stockInvestmentChecklistInst:
                #   for each in stockInvestmentChecklistInst:
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistSerializer(stockInvestmentChecklistInst)
                stockInvestmentChecklistInst_detail = stockInvestmentChecklistInst_detail.data
        except:
            stockInvestmentChecklistInst_list = None

        stock_detail["stockProfileNameSIC"] = stockInvestmentChecklistInst_detail

        stockIPOInst_details = ""
        try:
            stockIPOInst = stockIPO.objects.get(stockProfileName=stock)
            if stockIPOInst:
                #   for each in stockIPOInst:
                stockIPOInst_details = stockIPOSerializer(stockIPOInst)
                stockIPOInst_details = stockIPOInst_details.data
        except:
            stockIPOInst = None

        stock_detail["stockProfileNameSI"] = stockIPOInst_details

        stockDetailsInst_details = ""
        try:
            stockDetailsInst = stockDetails.objects.get(stockProfileName=stock)
            if stockDetailsInst:
                #   for each in stockDetailsInst:
                stockDetailsInst_details = stockDetailsSerializer(stockDetailsInst)
                stockDetailsInst_details = stockDetailsInst_details.data
        except:
            stockDetailsInst = None

        stock_detail["stockProfileNameSD"] = stockDetailsInst_details
        # createStockDetails = stockDetailsFormMergerAcquistion(instance=stockDetailsInst)
        # createSubsidiariesBusModelStockDetails = stockDetailsSubsidiariesBusModelForm(instance=stockDetailsInst)
        # createProductStockDetails = stockDetailsProductForm(instance=stockDetailsInst)
        # createAssestStockDetails = stockDetailsAssestForm(instance=stockDetailsInst)
        # createIndustryOverviewStockDetails = stockDetailsIndustryOverviewForm(instance=stockDetailsInst)
        # createStockAbout = stockDetailsAboutForm(instance=stockDetailsInst)
        # createawardsDescription = stockDetailsAwardForm(instance=stockDetailsInst)
        # createSSOTDescription = stockDetailsSSOTForm(instance=stockDetailsInst)

        revenueBreakupInst = stockRevenueBreakUp.objects.filter(stockProfileName=stock)
        revenueBreakupInst_list = []
        if revenueBreakupInst:
            for each in revenueBreakupInst:
                revenueBreakupInst_ser = stockRevenueBreakUpSerializer(each)
                revenueBreakupInst_list.append(revenueBreakupInst_ser.data)
        # viewStockRevenueBreakUpForm = stockRevenueBreakUpForm()
        stockFundingRoundsInst_list = []
        try:
            stockFundingRoundsInst = stockFundingRounds.objects.filter(stockProfileName=stock).order_by(
                '-dateOfInvestment')
            if stockFundingRoundsInst:
                for each in stockFundingRoundsInst:
                    stockFundingRoundsInst_ser = stockFundingRoundsSerializer(each)
                    stockFundingRoundsInst_list.append(stockFundingRoundsInst_ser.data)
        except:
            stockFundingInst = None

        stockFundingInst_detail = ""
        try:
            stockFundingInst = stockFunding.objects.get(stockProfileName=stock)
            if stockFundingInst:
                #   for each in stockFundingInst:
                stockFundingInst_detail = stockFundingSerializer(stockFundingInst)
                stockFundingInst_detail = stockFundingInst_detail.data
        except:
            stockFundingInst = None

        stock_detail['stockProfileNameSF'] = stockFundingInst_detail

        try:
            promotorHolding = stockOwnershipPattern.objects.get(stockProfileName=stock, year=currentYear)
            promotorHolding = promotorHolding.totalPromoterholdingValue
        except:
            promotorHolding = None
        try:
            # latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
            latestProfitAndLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')

            totalRevCY = latestProfitAndLoss.totalRevenue
            patCY = latestProfitAndLoss.netIncome
            epsCY = latestProfitAndLoss.basicEPS
            dps = latestProfitAndLoss.DPS
        except:
            totalRevCY = None
            patCY = None
            epsCY = None
            dps = None
        try:
            latestCashFlow = stockCashFlow.objects.filter(stockProfileName=stock).latest('year')
            cashFlowOperationsCY = latestCashFlow.cashFromOperatingActivities
            cashFlowFinancingCY = latestCashFlow.cashFromFinancingActivities
        except:
            cashFlowOperationsCY = None
            cashFlowFinancingCY = None

        categoryForEss = categoryOptions.objects.all().order_by('name')
        categoryForEss_list = []
        if categoryForEss:
            for each in categoryForEss:
                categoryForEss = categoryOptionsSerializer(each)
                categoryForEss_list.append(categoryForEss.data)
        sectorForEss = sectorOptions.objects.all().order_by('name')
        sectorForEss_list = []
        if sectorForEss:
            for each in sectorForEss:
                categoryForEss = sectorOptionsSerializer(each)
                sectorForEss_list.append(categoryForEss.data)
        subSectorForEss = subSectorOptions.objects.all().order_by('name')
        subSectorForEss_list = []
        if subSectorForEss:
            for each in subSectorForEss:
                subSectorForEss = subSectorOptionsSerializer(each)
                subSectorForEss_list.append(subSectorForEss.data)

        # Required changes in formuals Calculation starts  - done
        returnedGrowthROEVal = ROEgrowthCalculatorFrBankNBFCs(stock)
        intrinsicVal = intrinsicFormula(stock, forNBFC=True)
        # intrinsicVal = intrinsicFormulafrBankNBFCs(stock)
        returnedRevenueGrowthAlgoProgrammedData, processedNetProfitGrowthTextual = calGrowthTemplateDataViewFrBankNBFcs(
            stock, requestFrom='snapshot')
        # compoundSalesGrowth = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
        # compoundProfitGrowth = calculateProgrammedGrowth(processedNetProfitGrowthTextual)
        profitAndLossQuerySet = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')
        revenueGrowth = calculateGrowthNew(profitAndLossQuerySet, 'totalRevenue')
        compoundProfitGrowth = calculateGrowthNew(profitAndLossQuerySet, 'netIncome')
        # Required changes in formuals Calculation ends - done

        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        stockTransferDepositoryOptions_list = []
        try:
            if despositoryOptions:
                for each in despositoryOptions:
                    stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                    stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
        except:
            despositoryOptions = None
            stockTransferDepositoryOptions_list = []
        saleTypeOptions_list = []
        try:
            if saleType:
                for each in saleType:
                    saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                    saleTypeOptions_list.append(saleTypeOptions_ser.data)
        except:
            saleType = None
            saleTypeOptions_list = []

        bookValues_detail = ""
        try:
            bookValues = bookValueData.objects.filter(stockProfileName=stock).latest('year')
            if bookValues:
                #    for each in bookValues:
                bookValues_detail = bookValueDataSerializer(bookValues)
                bookValues_detail = bookValues_detail.data

            bookValYear = bookValues.year
            # totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=bookValYear)
            totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=bookValYear)
            bookValueCal = bookValues.bookValue / totalShareOutStandValueObj.totalCommonSharesOutstanding
        except:
            bookValues = bookValueCal = None

        fundingRoundsUnitInst_detail = ""
        try:
            fundingRoundsUnitInst = get_object_or_404(foundingRoundsFigureUnits, stockProfileName=stock)
            if fundingRoundsUnitInst:
                fundingRoundsUnitInst_detail = foundingRoundsFigureUnitsSerializer(fundingRoundsUnitInst)
                fundingRoundsUnitInst_detail = fundingRoundsUnitInst_detail.data
        except:
            fundingRoundsUnitInst = None
            fundingRoundsUnitInst_detail = ""

        fundingDetailsVisibilityInst_detail = ""
        try:
            fundingDetailsVisibilityInst = get_object_or_404(fundingDetailsVisibility, stockProfileName=stock)
            if fundingDetailsVisibilityInst:
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilitySerializer(fundingDetailsVisibilityInst)
                fundingDetailsVisibilityInst_detail = fundingDetailsVisibilityInst_detail.data
        except:
            fundingDetailsVisibilityInst = None
            fundingDetailsVisibilityInst_detail = ""

        stock_detail['stockProfileNameFDVI'] = fundingDetailsVisibilityInst_detail

        # fundingDetailsVisibilityCreate = fundingDetailsVisibilityForm()

        currentStockPrice = localOrScreenerPriceView(stock)

        if essentialInst:
            totalSharesInst = essentialInst.totalShares
        else:
            totalSharesInst = 0

        try:
            stockProfitAndLossInst = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            basicEps = stockProfitAndLossInst.basicEPS
            dilutedEps = stockProfitAndLossInst.dilutedEPS
        except:
            basicEps = 1
            dilutedEps = 1

        eps = check_eps_basic_or_diluted(basicEps, dilutedEps)
        decimalEPS = return_decimal_or_0(eps)
        if decimalEPS == 0:
            decimalEPS = 1
        try:
            PEvalue = round((currentStockPrice / decimalEPS), 2)
        except:
            PEvalue = None

        if bookValues:
            bookVal = bookValueCal
        else:
            bookVal = 1
        try:
            PBvalue = round((currentStockPrice / bookVal), 2)
        except:
            PBvalue = None

        try:
            earningsYield = round((epsCY / currentStockPrice) * 100, 2)
        except:
            earningsYield = None

        try:
            dividendYield = round((dps / currentStockPrice) * 100, 2)
        except:
            dividendYield = None
        try:
            latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            aumVals = latestBalanceSheet.aum
            aumGrowthVals = round(latestBalanceSheet.aumGrowth, 2)
        except:
            aumVals = None
            aumGrowthVals = None

        researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
        researchReportFAQsInst_list = []
        if len(researchReportFAQsInst):
            for each in researchReportFAQsInst:
                researchReportFAQs_serial = researchReportFAQsSerializer(each)
                researchReportFAQsInst_list.append(researchReportFAQs_serial.data)
        # researchReportFAQsInstForm = researchReportFAQsForm()

        # Enterprise Value
        cashAndShortTermEqui = minorityInt = 0
        try:
            stockBalanceSheetLatestObj = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            cashAndShortTermEqui = stockBalanceSheetLatestObj.cashAndCashEquivalents
            minorityInt = stockBalanceSheetLatestObj.minorityInterest

        except:
            pass
        balWithRBI = prefEquity = 0
        try:
            balWithRBI = essentialInst.balance_with_RBI
            prefEquity = essentialInst.preference_equity
        except:
            pass
        if not balWithRBI:
            balWithRBI = 0
        if not prefEquity:
            prefEquity = 0
        lgTermBorrow = curPortionOfLongTermDebt = srtTermBorrowings = leasLiability = 0
        try:
            latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
            if latestBalanceSheet.longTermBorrowings:
                lgTermBorrow = Decimal(latestBalanceSheet.longTermBorrowings)
            if latestBalanceSheet.currentPortionOfLongTermDebt:
                curPortionOfLongTermDebt = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
            if latestBalanceSheet.shortTermBorrowings:
                srtTermBorrowings = Decimal(latestBalanceSheet.shortTermBorrowings)
            if latestBalanceSheet.leaseLiability:
                leasLiability = Decimal(latestBalanceSheet.leaseLiability)
        except:
            pass
        totalDebt = lgTermBorrow + srtTermBorrowings + leasLiability + curPortionOfLongTermDebt
        try:
            marketCap = (totalSharesInst * currentStockPrice) / 10000000
        except:
            marketCap = None
        try:
            marketCapForEnterprise = numberConversion(marketCap, currentSystem='Cr',
                                                      convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            marketCapForEnterprise = None
        enterpriseVal = returnDecimalOrZero(marketCapForEnterprise) - (
                returnDecimalOrZero(cashAndShortTermEqui) - returnDecimalOrZero(balWithRBI)) + returnDecimalOrZero(
            totalDebt) + returnDecimalOrZero(prefEquity) + returnDecimalOrZero(minorityInt)
        try:
            enterpriseVal = numberConversion(enterpriseVal, currentSystem=stock.stockProfileNameFFU.financialNumbers,
                                             convertTo='Cr')
        except:
            pass

        totalShareYearlyDataInst = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                       shareType='financial_year').order_by('year')
        totalShareYearlyDataInst_list = []
        if len(totalShareYearlyDataInst):
            for each in totalShareYearlyDataInst:
                totalShareYearly_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInst_list.append(totalShareYearly_serial.data)
        totalShareYearlyDataInstConvertible = totalShareYearlyData.objects.filter(stockProfileName=stock,
                                                                                  shareType='convertible_equity').order_by(
            'year')
        totalShareYearlyDataInstConvertible_list = []
        if len(totalShareYearlyDataInstConvertible):
            for each in totalShareYearlyDataInstConvertible:
                totalShareYearlyData_serial = totalShareYearlyDataSerializer(each)
                totalShareYearlyDataInstConvertible_list.append(totalShareYearlyData_serial.data)
        # totalShareYearlyDataInstForm = totalShareYearlyDataForm()
        # commonFAQInstForm = commonFAQForm()
        commonFAQInst = commonFAQ.objects.all().order_by('id')
        commonFAQInst_list = []
        if len(commonFAQInst):
            for each in commonFAQInst:
                commonFAQInst_serial = commonFAQSerializer(each)
                commonFAQInst_list.append(commonFAQInst_serial.data)
        # researchReportFAQsInstForm = researchReportFAQsForm()
        # context = {
        #    'bookValues': bookValues_detail,
        # 'essentialInst': essentialInst_list,
        # 'createStockEssentials': createStockEssentials,
        # 'createStockEssentialsBottom': createStockEssentialsBottom,
        # 'stockInvestmentChecklistInst': stockInvestmentChecklistInst_list,
        # 'createstockInvestmentChecklist': createstockInvestmentChecklist,
        # 'stockIPOInst': stockIPOInst_list,
        # 'createStockIPO': createStockIPO,
        # 'stockDetailsInst': stockDetailsInst_list,
        # 'createStockDetails': createStockDetails,
        # 'createSubsidiariesBusModelStockDetails': createSubsidiariesBusModelStockDetails,
        # 'createProductStockDetails': createProductStockDetails,
        # 'createAssestStockDetails': createAssestStockDetails,
        # 'createIndustryOverviewStockDetails': createIndustryOverviewStockDetails,
        # 'stockFundingInst': stockFundingInst_list,
        # 'createStockFunding': createStockFunding,
        #    'stockFundingRoundsInst': stockFundingRoundsInst_list,
        # 'createStockFundingRounds': createStockFundingRounds,
        #    'promotorHolding': promotorHolding,
        #    'stockAdmInst': stockAdmInst_detail,
        # 'createStockAdmin': createStockAdmin,
        # 'createStockAdminSnapshot': createStockAdminSnapshot,
        # 'createStockAbout': createStockAbout,
        # 'createawardsDescription': createawardsDescription,
        # 'createSSOTDescription': createSSOTDescription,
        #    'compoundSalesGrowth': revenueGrowth,
        #    'compoundProfitGrowth': compoundProfitGrowth,
        #    'totalRevCY': totalRevCY,
        #    'patCY': patCY,
        #    'epsCY': epsCY,
        #    'cashFlowOperationsCY': cashFlowOperationsCY,
        #    'cashFlowFinancingCY': cashFlowFinancingCY,
        #    'categoryForEss': categoryForEss_list,
        #    'sectorForEss': sectorForEss_list,
        #    'subSectorForEss': subSectorForEss_list,
        #    'returnedGrowthROEVal': returnedGrowthROEVal,
        #    'intrinsicVal': intrinsicVal,
        #    'revenueBreakupInst': revenueBreakupInst_list,
        # 'viewStockRevenueBreakUpForm': viewStockRevenueBreakUpForm,
        #    'despositoryOptions': stockTransferDepositoryOptions_list,
        #    'saleType': saleTypeOptions_list,
        #    'stock': stock_detail,
        #    'fundingRoundsUnitInst': fundingRoundsUnitInst_detail,
        # 'fundingRoundsUnitCreate': fundingRoundsUnitCreate,
        # 'fundingDetailsVisibilityInst': fundingDetailsVisibilityInst,
        # 'fundingDetailsVisibilityCreate': fundingDetailsVisibilityCreate,
        #    'benGrahamOrDCFInst': benGrahamOrDCFInst_detail,
        # 'benGrahamOrDCFForm': benGrahamOrDCFCreate,
        #    'marketCap': marketCap,
        #    'PEvalue': PEvalue,
        #    'PBvalue': PBvalue,
        #    'earningsYield': earningsYield,
        #    'dividendYield': dividendYield,
        #    'bookValueCal': bookValueCal,
        #    'aumVals': aumVals,
        #    'aumGrowthVals': aumGrowthVals,
        #    'researchReportFAQsInst': researchReportFAQsInst_list,
        # 'researchReportFAQsInstForm': researchReportFAQsInstForm,
        #    'enterpriseVal': enterpriseVal,
        #    'totalShareYearlyDataInst': totalShareYearlyDataInst_list,
        #    'totalShareYearlyDataInstConvertible': totalShareYearlyDataInstConvertible_list,
        # 'totalShareYearlyDataInstForm': totalShareYearlyDataInstForm,
        #    'commonFAQInst': commonFAQInst_list,
        # 'commonFAQInstForm': commonFAQInstForm,
        # 'researchReportFAQsInstForm': researchReportFAQsInstForm,
        # }
        returnedRevenueGrowthAlgoProgrammedData, processedNetProfitGrowthTextual = calGrowthTemplateDataView(stock,
                                                                                                             requestFrom='snapshot')
        compoundSalesGrowth = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)

        try:
            foundingRoundsFigureUnitsInst = foundingRoundsFigureUnits.objects.get(stockProfileName=stock)
        except:
            foundingRoundsFigureUnitsInst = None

        response_dict = {}
        stock_detail = {}
        stock_detail['data'] = {}
        if stock_serialized:
            saleType_list = []
            for each in stock_serialized['saleType']:
                try:
                    saleType_list.append(get_object_or_404(saleTypeOptions, id=each).name)
                except:
                    saleType_list.append(each)
            stock_detail['data']['saleType'] = saleType_list
            pass

        if stockFundingInst_detail:
            stock_detail['data']['stage'] = stockFundingInst_detail['stage']
            stock_detail['data']['lookingFor'] = stockFundingInst_detail['lookingFor']
        else:
            stock_detail['data']['stage'] = None
            stock_detail['data']['lookingFor'] = None

        if aumVals:
            stock_detail['data']['aum'] = aumVals
        if aumGrowthVals:
            stock_detail['data']['aumGrowth'] = aumGrowthVals
        if financialFigureUnitsInst_detail and 'financialNumbers' in financialFigureUnitsInst_detail:
            stock_detail['data']['financialNumbers'] = financialFigureUnitsInst_detail['financialNumbers']
        if benGrahamOrDCFInst_detail:
            stock_detail['data']['benGrahamOrDCFInst'] = benGrahamOrDCFInst_detail

        if stock.content:
            stock_detail['SEOContent'] = stock.content
        if stock.seoTitle:
            stock_detail['seoTitle'] = stock.seoTitle
        if stockDetailsInst_details or stockDetailsInst_details != "" or stockDetailsInst_details != []:
            stock_detail["stockProfileNameSD"] = stockDetailsInst_details
        if fundingDetailsVisibilityInst_detail or fundingDetailsVisibilityInst_detail != "" or fundingDetailsVisibilityInst_detail != []:
            stock_detail['stockProfileNameFDVI'] = fundingDetailsVisibilityInst_detail

        stock_detail['essentials'] = {'label': 'Essentials', 'data': {}, 'child': {}}
        if "ISIN" in essentialInst_detail and essentialInst_detail["ISIN"] != "":
            stock_detail['essentials']['data']['ISIN'] = essentialInst_detail["ISIN"]
        if "faceValue" in essentialInst_detail and essentialInst_detail["faceValue"] != "":
            stock_detail['essentials']['data']['faceValue'] = essentialInst_detail["faceValue"]
        if "totalShares" in essentialInst_detail and essentialInst_detail["totalShares"] != "":
            stock_detail['essentials']['data']['totalShares'] = essentialInst_detail["totalShares"]
        if "essentialsDescription" in essentialInst_detail and essentialInst_detail["essentialsDescription"] != "":
            stock_detail['essentials']['data']['essentialsDescription'] = essentialInst_detail["essentialsDescription"]
        if totalRevCY:
            stock_detail['essentials']['data']['totalRevCY'] = totalRevCY
        if patCY:
            stock_detail['essentials']['data']['patCY'] = patCY
        if epsCY:
            stock_detail['essentials']['data']['epsCY'] = epsCY
        if PEvalue:
            stock_detail['essentials']['data']['PEvalue'] = PEvalue
        if PBvalue:
            stock_detail['essentials']['data']['PBvalue'] = PBvalue
        if marketCap:
            stock_detail['essentials']['data']['marketCap'] = marketCap
        if enterpriseVal:
            stock_detail['essentials']['data']['enterpriseVal'] = enterpriseVal
        if bookValueCal:
            stock_detail['essentials']['data']['bookValueCal'] = bookValueCal
        if intrinsicVal:
            stock_detail['essentials']['data']['intrinsicVal'] = intrinsicVal
        if dividendYield:
            stock_detail['essentials']['data']['dividendYield'] = dividendYield
        if earningsYield:
            stock_detail['essentials']['data']['earningsYield'] = earningsYield
        if promotorHolding:
            stock_detail['essentials']['data']['promotorHolding'] = promotorHolding
        if 'sector' in essentialInst_detail and essentialInst_detail['sector'] != "":
            try:
                stock_detail['essentials']['data']['sector'] = get_object_or_404(sectorOptions,
                                                                                 id=essentialInst_detail['sector']).name
            except:
                stock_detail['essentials']['data']['sector'] = essentialInst_detail['sector']
        if 'subSector' in essentialInst_detail and essentialInst_detail['subSector'] != "":
            try:
                stock_detail['essentials']['data']['subSector'] = get_object_or_404(subSectorOptions,
                                                                                    id=essentialInst_detail[
                                                                                        'subSector']).name
            except:
                stock_detail['essentials']['data']['subSector'] = essentialInst_detail['subSector']
        if 'category' in essentialInst_detail and essentialInst_detail['category'] != "":
            try:
                stock_detail['essentials']['data']['category'] = get_object_or_404(categoryOptions,
                                                                                   id=essentialInst_detail[
                                                                                       'category']).name
            except:
                stock_detail['essentials']['data']['category'] = essentialInst_detail['category']
        if cashFlowOperationsCY:
            stock_detail['essentials']['data']['cashFlowOperationsCY'] = cashFlowOperationsCY
        if cashFlowFinancingCY:
            stock_detail['essentials']['data']['cashFlowFinancingCY'] = cashFlowFinancingCY
        if 'salesGrowthRateOfXYear' in essentialInst_detail and essentialInst_detail['salesGrowthRateOfXYear'] != "":
            stock_detail['essentials']['data']['salesGrowthRateOfXYear'] = essentialInst_detail[
                'salesGrowthRateOfXYear']

        if stock_detail['essentials']['data'] == {} and stock_detail['essentials']['child'] == {}:
            stock_detail.pop('essentials')

        if totalShareYearlyDataInst_list and totalShareYearlyDataInst_list != [] and totalShareYearlyDataInstConvertible_list and totalShareYearlyDataInstConvertible_list != []:
            stock_detail['totalShareYearlyData'] = {'label': 'Total Share Yearly Data', 'data': {}, 'child': {}}
            totalShareYearlyData_list = []
            for item in totalShareYearlyDataInst_list:
                temp = {}
                temp['shareType'] = item['shareType']
                temp['year'] = item['year']
                temp['totalShares'] = item['totalShares']
                # temp['fundName'] = item['fundName']
                # temp['fundingAmount'] = item['fundingAmount']
                # temp['currencySymbol'] = get_object_or_404(currencySymbolOptions, id=item['currencySymbol']).uniqueCode
                # temp['fundingUnitNumbers'] = None
                totalShareYearlyData_list.append(temp)

            totalShareYearlyDataConvertible_list = []
            for item in totalShareYearlyDataInstConvertible_list:
                temp = {}
                temp['shareType'] = item['shareType']
                temp['year'] = item['year']
                temp['totalShares'] = item['totalShares']
                # temp['fundName'] = item['fundName']
                # temp['fundingAmount'] = item['fundingAmount']
                # temp['currencySymbol'] = get_object_or_404(currencySymbolOptions, id=item['currencySymbol']).uniqueCode
                # temp['fundingUnitNumbers'] = None
                totalShareYearlyDataConvertible_list.append(temp)
            # totalShareYearlyDataInstConvertible_list
            stock_detail['totalShareYearlyData']['data']['totalShareYearlyData'] = totalShareYearlyData_list
            stock_detail['totalShareYearlyData']['data'][
                'totalShareYearlyDataConvertible'] = totalShareYearlyDataConvertible_list

        stock_detail['growth'] = {'label': "Growth", 'data': {}, 'child': {}}
        if revenueGrowth and revenueGrowth != {}:
            stock_detail['growth']['data']['revenueGrowth'] = revenueGrowth
        if compoundSalesGrowth and compoundSalesGrowth != {}:
            stock_detail['growth']['data']['compoundSalesGrowth'] = compoundSalesGrowth
        if compoundProfitGrowth and compoundProfitGrowth != {}:
            stock_detail['growth']['data']['compoundProfitGrowth'] = compoundProfitGrowth
        if returnedGrowthROEVal and returnedGrowthROEVal != {}:
            stock_detail['growth']['data']['returnedGrowthROEVal'] = returnedGrowthROEVal

        if stock_detail['growth']['data'] == {} and stock_detail['growth']['child'] == {}:
            stock_detail.pop('growth')

        stock_detail['about'] = {'label': 'About', 'data': {}, 'child': {}}
        if stock_detail['about']['data'] == {} and stock_detail['about']['child'] == {}:
            stock_detail.pop('about')

        if stockIPOInst_details and stockIPOInst_details != {}:
            stock_detail['IPODetails'] = {'label': 'IPO Details', 'data': {'stockProfileNameSI': stockIPOInst_details},
                                          'child': {}}

        if stockFundingRoundsInst_list and stockFundingRoundsInst_list != []:
            stock_detail['funding'] = {'label': 'Funding', 'data': {}, 'child': {}}
            fundingRounds_list = []
            for item in stockFundingRoundsInst_list:
                temp = {}
                temp['fundingRound'] = item['fundingRound']
                temp['dateOfInvestment'] = item['dateOfInvestment']
                temp['date_available'] = item['date_available']
                temp['fundedBy'] = item['fundedBy']
                temp['fundName'] = item['fundName']
                temp['fundingAmount'] = item['fundingAmount']
                try:
                    temp['fundingUnitNumbers'] = foundingRoundsFigureUnitsInst.fundingUnitNumbers
                except:
                    temp['fundingUnitNumbers'] = None
                try:
                    temp['currencySymbol'] = get_object_or_404(currencySymbolOptions,
                                                               id=item['currencySymbol']).uniqueCode
                except:
                    temp['currencySymbol'] = item['currencySymbol']
                fundingRounds_list.append(temp)

            stock_detail['funding']['data']['fundingRounds'] = fundingRounds_list

        stock_detail['merger&Acquisition'] = {'label': 'Merger & Acquisition', 'data': {}, 'child': {}}
        if 'mergerDescription' in stockDetailsInst_details and stockDetailsInst_details['mergerDescription'] != "":
            stock_detail['merger&Acquisition']['data']['mergerDescription'] = stockDetailsInst_details[
                'mergerDescription']
        if 'aquistionsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'aquistionsDescription'] != "":
            stock_detail['merger&Acquisition']['data']['aquistionsDescription'] = stockDetailsInst_details[
                'aquistionsDescription']
        if 'investmentsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'investmentsDescription'] != "":
            stock_detail['merger&Acquisition']['data']['investmentsDescription'] = stockDetailsInst_details[
                'investmentsDescription']

        if stock_detail['merger&Acquisition']['data'] == {} and stock_detail['merger&Acquisition']['child'] == {}:
            stock_detail.pop('merger&Acquisition')

        stock_detail['subsidiaries'] = {'label': 'Subsidiaries', 'data': {}, 'child': {}}
        if 'subsidiaryDescription' in stockDetailsInst_details:
            stock_detail['subsidiaries']['data']['subsidiaryDescription'] = stockDetailsInst_details[
                'subsidiaryDescription']

        if stock_detail['subsidiaries']['data'] == {} and stock_detail['subsidiaries']['child'] == {}:
            stock_detail.pop('subsidiaries')

        stock_detail['businessModel'] = {'label': 'Business Model', 'data': {}, 'child': {}}
        if 'businessModelDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'businessModelDescription'] != "":
            stock_detail['businessModel']['data']['businessModelDescription'] = stockDetailsInst_details[
                'businessModelDescription']

        if stock_detail['businessModel']['data'] == {} and stock_detail['businessModel']['child'] == {}:
            stock_detail.pop('businessModel')

        if revenueBreakupInst_list and revenueBreakupInst_list != []:
            stock_detail['revenueSegmentation'] = {'label': 'Revenue Segmentation',
                                                   'data': {'revenueBreakupInst': revenueBreakupInst_list}, 'child': {}}

        stock_detail['product&Services'] = {'label': 'Product & Services', 'data': {}, 'child': {}}
        if 'productsAndServicesDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'productsAndServicesDescription'] != "":
            stock_detail['product&Services']['data']['ProductsAndServicesDescription'] = stockDetailsInst_details[
                'productsAndServicesDescription']

        if stock_detail['product&Services']['data'] == {} and stock_detail['product&Services']['child'] == {}:
            stock_detail.pop('product&Services')

        stock_detail['assets'] = {'label': 'Assets', 'data': {}, 'child': {}}
        if 'assestsDescription' in stockDetailsInst_details and stockDetailsInst_details['assestsDescription'] != "":
            stock_detail['assets']['data']['assestsDescription'] = stockDetailsInst_details['assestsDescription']

        if stock_detail['assets']['data'] == {} and stock_detail['assets']['child'] == {}:
            stock_detail.pop('assets')

        stock_detail['industryOverview'] = {'label': 'Industry Overview', 'data': {}, 'child': {}}
        if 'industryStatisticsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'industryStatisticsDescription'] != "":
            stock_detail['industryOverview']['child']['industryStatisticsDescription'] = {
                'label': 'Industry Statistics Description',
                'data': {'industryStatisticsDescription': stockDetailsInst_details['industryStatisticsDescription']},
                'child': {}}
        # stock_detail['industryOverview']['child']['industryStatisticsDescription']['data']['industryStatisticsDescription'] = stockDetailsInst_details['industryStatisticsDescription']
        if 'futureProspectsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'futureProspectsDescription'] != "":
            stock_detail['industryOverview']['child']['futureProspectsDescription'] = {
                'label': 'Future Prospects Description',
                'data': {'futureProspectsDescription': stockDetailsInst_details['futureProspectsDescription']},
                'child': {}}
        # stock_detail['industryOverview']['child']['futureProspectsDescription']['data']['futureProspectsDescription'] = stockDetailsInst_details['futureProspectsDescription']
        if 'governmentInitiativesDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'governmentInitiativesDescription'] != "":
            stock_detail['industryOverview']['child']['governmentInitiativesDescription'] = {
                'label': 'Government Initiatives Description', 'data': {
                    'governmentInitiativesDescription': stockDetailsInst_details['governmentInitiativesDescription']},
                'child': {}}
        # stock_detail['industryOverview']['child']['governmentInitiativesDescription']['data']['governmentInitiativesDescription'] = stockDetailsInst_details['governmentInitiativesDescription']
        if stock_detail['industryOverview']['data'] == {} and stock_detail['industryOverview']['child'] == {}:
            stock_detail.pop('industryOverview')

        stock_detail['awards&Achievements'] = {'label': 'Awards & Achievements', 'data': {}, 'child': {}}
        if 'awardsDescription' in stockDetailsInst_details and stockDetailsInst_details['awardsDescription'] != "":
            stock_detail['awards&Achievements']['data']['awardsDescription'] = stockDetailsInst_details[
                'awardsDescription']
        if stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail != "":
            stock_detail['awards&Achievements']['data']['stockProfileNameSIC'] = stockInvestmentChecklistInst_detail

        if stock_detail['awards&Achievements']['data'] == {} and stock_detail['awards&Achievements']['child'] == {}:
            stock_detail.pop('awards&Achievements')

        stock_detail['swot'] = {'label': 'SWOT', 'data': {}, 'child': {}}
        if 'strengthsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'strengthsDescription'] != "":
            stock_detail['swot']['child']['strengthsDescription'] = {'label': 'Strengths Description', 'data': {
                'strengthsDescription': stockDetailsInst_details['strengthsDescription']}, 'child': {}}
        # stock_detail['swot']['child']['strengthsDescription']['data']['strengthsDescription'] = stockDetailsInst_details['strengthsDescription']
        if 'shortcomingsDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'shortcomingsDescription'] != "":
            stock_detail['swot']['child']['shortcomingsDescription'] = {'label': 'Shortcomings Description', 'data': {
                'shortcomingsDescription': stockDetailsInst_details['shortcomingsDescription']}, 'child': {}}
        # stock_detail['swot']['child']['shortcomingsDescription']['data']['shortcomingsDescription'] = stockDetailsInst_details['shortcomingsDescription']
        if 'opportunitiesDescription' in stockDetailsInst_details and stockDetailsInst_details[
            'opportunitiesDescription'] != "":
            stock_detail['swot']['child']['opportunitiesDescription'] = {'label': 'Opportunities Description', 'data': {
                'opportunitiesDescription': stockDetailsInst_details['opportunitiesDescription']}, 'child': {}}
        # stock_detail['swot']['child']['opportunitiesDescription']['data']['opportunitiesDescription'] = stockDetailsInst_details['opportunitiesDescription']
        if 'threatsDescription' in stockDetailsInst_details and stockDetailsInst_details['threatsDescription'] != "":
            stock_detail['swot']['child']['threatsDescription'] = {'label': 'Threats Description', 'data': {
                'threatsDescription': stockDetailsInst_details['threatsDescription']}, 'child': {}}
        # stock_detail['swot']['child']['threatsDescription']['data']['threatsDescription'] = stockDetailsInst_details['threatsDescription']

        if stock_detail['swot']['data'] == {} and stock_detail['swot']['child'] == {}:
            stock_detail.pop('swot')

        stock_detail['investmentChecklist'] = {'label': 'Investment Checklist', 'data': {}, 'child': {}}
        if 'management' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'management'] != "":
            stock_detail['investmentChecklist']['data']['management'] = stockInvestmentChecklistInst_detail[
                'management']
        if 'acountingPratice' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'acountingPratice'] != "":
            stock_detail['investmentChecklist']['data']['acountingPratice'] = stockInvestmentChecklistInst_detail[
                'acountingPratice']
        if 'profitability' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'profitability'] != "":
            stock_detail['investmentChecklist']['data']['profitability'] = stockInvestmentChecklistInst_detail[
                'profitability']
        if 'solvency' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail['solvency'] != "":
            stock_detail['investmentChecklist']['data']['solvency'] = stockInvestmentChecklistInst_detail['solvency']
        if 'growth' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail['growth'] != "":
            stock_detail['investmentChecklist']['data']['growth'] = stockInvestmentChecklistInst_detail['growth']
        if 'valuation' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'valuation'] != "":
            stock_detail['investmentChecklist']['data']['valuation'] = stockInvestmentChecklistInst_detail['valuation']
        if 'businessType' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'businessType'] != "":
            try:
                stock_detail['investmentChecklist']['data']['businessType'] = get_object_or_404(businessTypeOptions, id=
                stockInvestmentChecklistInst_detail['businessType']).name
            except:
                stock_detail['investmentChecklist']['data']['businessType'] = stockInvestmentChecklistInst_detail[
                    'businessType']
        if 'rating' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail['rating'] != "":
            stock_detail['investmentChecklist']['data']['rating'] = stockInvestmentChecklistInst_detail['rating']
        if 'recommendation' in stockInvestmentChecklistInst_detail and stockInvestmentChecklistInst_detail[
            'recommendation'] != "":
            try:
                stock_detail['investmentChecklist']['data']['recommendation'] = get_object_or_404(recommendationOptions,
                                                                                                  id=
                                                                                                  stockInvestmentChecklistInst_detail[
                                                                                                      'recommendation']).name
            except:
                stock_detail['investmentChecklist']['data']['recommendation'] = stockInvestmentChecklistInst_detail[
                    'recommendation']
        if 'accumulationRangeDescriptionFrom' in stockInvestmentChecklistInst_detail and \
                stockInvestmentChecklistInst_detail['accumulationRangeDescriptionFrom'] != "":
            stock_detail['investmentChecklist']['data']['accumulationRangeDescriptionFrom'] = \
            stockInvestmentChecklistInst_detail['accumulationRangeDescriptionFrom']
        if 'accumulationRangeDescriptionTo' in stockInvestmentChecklistInst_detail and \
                stockInvestmentChecklistInst_detail['accumulationRangeDescriptionTo'] != "":
            stock_detail['investmentChecklist']['data']['accumulationRangeDescriptionTo'] = \
            stockInvestmentChecklistInst_detail['accumulationRangeDescriptionTo']

        if stock_detail['investmentChecklist']['data'] == {} and stock_detail['investmentChecklist']['child'] == {}:
            stock_detail.pop('investmentChecklist')

        stock_detail['detailInfo'] = {'label': 'Detail Info', 'data': {}, 'child': {}}
        if 'typeOfCompany' in essentialInst_detail and essentialInst_detail['typeOfCompany'] != "":
            try:
                stock_detail['detailInfo']['data']['typeOfCompany'] = get_object_or_404(typeOfCompanyOptions,
                                                                                        id=essentialInst_detail[
                                                                                            'typeOfCompany']).name
            except:
                stock_detail['detailInfo']['data']['typeOfCompany'] = essentialInst_detail['typeOfCompany']
        if 'countryRegisteredIn' in essentialInst_detail and essentialInst_detail['countryRegisteredIn'] != "":
            try:
                stock_detail['detailInfo']['data']['countryRegisteredIn'] = get_object_or_404(countryOptions,
                                                                                              id=essentialInst_detail[
                                                                                                  'countryRegisteredIn']).name
            except:
                stock_detail['detailInfo']['data']['countryRegisteredIn'] = essentialInst_detail['countryRegisteredIn']
        if 'registeredDate' in essentialInst_detail and essentialInst_detail['registeredDate'] != "":
            stock_detail['detailInfo']['data']['registeredDate'] = essentialInst_detail['registeredDate']
        if 'researchLastUpdatedOn' in essentialInst_detail and essentialInst_detail['researchLastUpdatedOn'] != "":
            stock_detail['detailInfo']['data']['researchLastUpdatedOn'] = essentialInst_detail['researchLastUpdatedOn']
        if 'listingDate' in essentialInst_detail and essentialInst_detail['listingDate'] != "":
            stock_detail['detailInfo']['data']['listingDate'] = essentialInst_detail['listingDate']
        if 'stockExchangeReferenceSymbol' in essentialInst_detail and essentialInst_detail[
            'stockExchangeReferenceSymbol'] != "":
            stock_detail['detailInfo']['data']['stockExchangeReferenceSymbol'] = essentialInst_detail[
                'stockExchangeReferenceSymbol']
        if 'regOffice' in essentialInst_detail and essentialInst_detail['regOffice'] != "":
            stock_detail['detailInfo']['data']['regOffice'] = essentialInst_detail['regOffice']
        if 'website' in essentialInst_detail and essentialInst_detail['website'] != "":
            stock_detail['detailInfo']['data']['website'] = essentialInst_detail['website']

        if stock_detail['detailInfo']['data'] == {} and stock_detail['detailInfo']['child'] == {}:
            stock_detail.pop('detailInfo')

        response_dict.update({"stock": stock_detail})

        return Response({'response': response_dict})


@api_view(['GET'])
def getKeyRatioView_01(request, slug):
    stock_detail = ""
    response_dict = {}
    stock = get_object_or_404(stockBasicDetail, id=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')
    renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
    if renderBankNBFCsTemplates:
        return redirect('stockApp:keyRatioForBankNBFCsApi', slug)
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
        # Stock_id  = stock_detail['id']
    stockProfitLoss_list = []
    stockProfitLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if stockProfitLoss:
            for each in stockProfitLoss:
                stockProfitLoss_ser = stockProfitAndLossSerializer(each)
                stockProfitLoss_list.append(stockProfitLoss_ser.data)
    except:
        stockProfitLoss = None
        stockProfitLoss_list = []
    stockBalanceSheet_list = []
    balanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if balanceSheet:
            for each in balanceSheet:
                stockBalanceSheet_ser = stockBalanceSheetSerializer(each)
                stockBalanceSheet_list.append(stockBalanceSheet_ser.data)
    except:
        balanceSheet = None
        stockBalanceSheet_list = []
    stockCashFlow_list = []
    cashFlow = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if cashFlow:
            for each in cashFlow:
                stockCashFlow_ser = stockCashFlowSerializer(each)
                stockCashFlow_list.append(stockCashFlow_ser.data)
    except:
        cashFlow = None
        stockCashFlow_list = []
    deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgIntangibleAssetDict, avgROceDenoPart = stockBalanceSheetCalculation(
        stock)
    interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict = stockProfitAndLossCalculation(
        stock)
    returnOnEquity = {}
    roce = {}
    returnOnAssets = {}
    dividentYield = {}
    earningYield = {}
    for key, val in netIncomeDict.items():
        val2 = averageTotalEquityDict.get(key)
        if val2:
            valEquity = val2
        else:
            valEquity = 1
        catROERounded = round((val / valEquity) * 100, 2)
        returnOnEquity[key] = catROERounded
    for item in stockProfitLoss:
        currentStockPrice = localOrScreenerPriceView(stock)
        # try:
        #         currentStockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
        #         currentStockPrice = currentStockPriceInst.investorPrice
        # except:
        #         currentStockPrice = 0
        # divident
        try:
            DPSforThisYear = item.DPS
        except:
            DPSforThisYear = None
        calDividentforThisYear = dividentYieldGraphView(DPSforThisYear, currentStockPrice)
        if calDividentforThisYear:
            dividentYield[item.year] = calDividentforThisYear
        # earning
        calEPSforThisYear = check_eps_basic_or_diluted(item.basicEPS, item.dilutedEPS)
        calEarningforThisYear = earningYieldGraphView(calEPSforThisYear, currentStockPrice)
        if calEarningforThisYear:
            earningYield[item.year] = calEarningforThisYear
    # Ishima pointers changes for ROCE starts
    # for key, val in pbitDict.items():
    #         val2 = averageTotalEquityDict.get(key)
    #         val3 = avgROceDenoPart.get(key)
    #         avgROceDenoPart
    #         if val2:
    #                 valAverageEquity = val2
    #         else :
    #                 valAverageEquity = 0

    #         if val3:
    #                 valNonCurrentLiab = val3
    #         else :
    #                 valNonCurrentLiab = 0

    # sumofEquityAndNonCrrLiabilities = valAverageEquity + valNonCurrentLiab
    # if not sumofEquityAndNonCrrLiabilities:
    #         sumofEquityAndNonCrrLiabilities = 1
    # roce[key] = round((val / ( sumofEquityAndNonCrrLiabilities )) * 100,2)
    # Ishima pointers changes for ROCE ends
    for key, val in pbitDict.items():
        val2 = avgTotalAssetDict.get(key)
        val3 = avgROceDenoPart.get(key)
        avgROceDenoPart
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0

        if val3:
            valCurrentLiab = val3
        else:
            valCurrentLiab = 0

        sumofAssestAndCrrLiabilities = valAverageAsset - valCurrentLiab
        if not sumofAssestAndCrrLiabilities:
            sumofAssestAndCrrLiabilities = 1
        roce[key] = round((val / (sumofAssestAndCrrLiabilities)) * 100, 2)
    for key, val in netIncomeDict.items():
        val2 = avgTotalAssetDict.get(key)
        val3 = avgIntangibleAssetDict.get(key)
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0
        if val3:
            valAverageIntangibleAsset = val3
        else:
            valAverageIntangibleAsset = 0
        # processedVal = valAverageAsset - valAverageIntangibleAsset
        # changes from Kulmehar starts
        processedVal = valAverageAsset
        # chnages from Kulmehar ends
        if processedVal == 0:
            processedVal = 1
        returnOnAssets[key] = round((val / processedVal) * 100, 2)

    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
            stockAdmInst_detail = stockAdmInst_detail.data
        # print("stockAdmInst", stockAdmInst)
    except:
        stockAdmInst = None
        stockAdmInst_detail = ""

    stockGrowthInst_detail = ""
    try:
        stockGrowthInst = stockGrowth.objects.get(stockProfileName=stock)
        if stockGrowthInst:
            stockGrowthInst_detail = stockGrowthSerializer(stockGrowthInst)
            stockGrowthInst_detail = stockGrowthInst_detail.data
        # print("stockGrowthInst", stockGrowthInst)
    except:
        stockGrowthInst = None
        stockGrowthInst_detail = ""

    # createStockGrowth = stockGrowthForm(instance=stockGrowthInst)
    stockSolvencyInst_detail = ""
    try:
        stockSolvencyInst = stockSolvency.objects.get(stockProfileName=stock)
        if stockSolvencyInst:
            stockSolvencyInst_detail = stockSolvencySerializer(stockSolvencyInst)
            stockSolvencyInst_detail = stockSolvencyInst_detail.data
        # print("stockSolvencyInst", stockSolvencyInst)
    except:
        stockSolvencyInst = None
        stockSolvencyInst_detail = ""
    # createStockSolvency = stockSolvencyForm(instance=stockSolvencyInst)
    stockOperatingEfficiencyInst_detail = ""
    try:
        stockOperatingEfficiencyInst = stockOperatingEfficiency.objects.get(stockProfileName=stock)
        if stockOperatingEfficiencyInst:
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencySerializer(stockOperatingEfficiencyInst)
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencyInst_detail.data
        # print("stockOperatingEfficiencyInst", stockOperatingEfficiencyInst)
    except:
        stockOperatingEfficiencyInst = None
        stockOperatingEfficiencyInst_detail = ""
    # createStockOperatingEfficiency = stockOperatingEfficiencyForm(instance=stockOperatingEfficiencyInst)
    sectorSpecificRatiosInst_detail = ""
    try:
        sectorSpecificRatiosInst = sectorSpecificRatios.objects.get(stockProfileName=stock)
        if sectorSpecificRatiosInst:
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosSerializer(sectorSpecificRatiosInst)
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosInst_detail.data
        # print('sectorSpecificRatiosInst', sectorSpecificRatiosInst)
    except:
        sectorSpecificRatiosInst = None
        sectorSpecificRatiosInst_detail = ""
    # createSectorSpecificRatios = sectorSpecificRatiosForm(instance=sectorSpecificRatiosInst)
    stockRatiosInst_detail = ""
    try:
        stockRatiosInst = stockRatios.objects.get(stockProfileName=stock)
        if stockRatiosInst:
            stockRatiosInst_detail = stockRatiosSerializer(stockRatiosInst)
            stockRatiosInst_detail = stockRatiosInst_detail.data
        # print('stockRatiosInst', stockRatiosInst)
    except:
        stockRatiosInst = None
        stockRatiosInst_detail = ""
    despositoryOptions, saleType = rightSideMenuObjs()
    stockTransferDepositoryOptions_list = []
    try:
        if despositoryOptions:
            for each in despositoryOptions:
                stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
    except:
        despositoryOptions = None
        stockTransferDepositoryOptions_list = []
    saleTypeOptions_list = []
    try:
        if saleType:
            for each in saleType:
                saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                saleTypeOptions_list.append(saleTypeOptions_ser.data)
    except:
        saleType = None
        saleTypeOptions_list = []
    # createStockRatios = stockRatiosForm(instance=stockRatiosInst)
    returnedGrowthDataRevenue, returnedRevenueGrowthAlgoProgrammedData, returnedNetProfitGrowthData, returnedNetProfitAlgoProgrammedData, returnedEPSGrowthData, returnedEPSAlgoProgrammedData, returnedEBITDAGrowthData, returnedEBITDAAlgoProgrammedData, returnedPBITGrowthData, returnedPBITAlgoProgrammedData = calGrowthTemplateDataView(
        stock)
    processedRevenueGrowthTextual = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    processedNetProfitGrowthTextual = calculateProgrammedGrowth(returnedNetProfitAlgoProgrammedData)
    processedEPSGrowthTextual = calculateProgrammedGrowth(returnedEPSAlgoProgrammedData)
    processedEBITDAGrowthTextual = calculateProgrammedGrowth(returnedEBITDAAlgoProgrammedData)
    processedPBITGrowthTextual = calculateProgrammedGrowth(returnedPBITAlgoProgrammedData)
    processedBookValueGrowthTextual = growthCalculatorForAnnualValues(stock, growthFor='bookValue')
    processedAssetGrowthTextual = growthCalculatorForAnnualValues(stock, growthFor='assetGrowth')
    processedCashFlowGrowthTextual, processedCashFlowGrowthFinancingTextual = growthCalculatorForAnnualValues(stock,
                                                                                                              growthFor='cashFlow')
    indusSpecificGraphs = industrySpecificGraphs.objects.filter(stockProfileName=stock)
    industrySpecificGraph = industrySpecificGraphForm()
    industrySpecificValsGraph = industrySpecificGraphValsForm()
    indusGraphDict = {}
    for graph in indusSpecificGraphs:
        # indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:7]
        indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:10]
        # indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('-year')[0:7]
        indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by(
            '-year')[0:10]
        graphDict = {}
        dataDict = {}
        growthGraphDict = {}
        forCount = 0
        if graph.graphType == 'Value':
            graphDict['type'] = 'Value'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                forCount += 1
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
            for yearlyItemsGrowth in indusSpecificValsGraphsForGrowth:
                growthGraphDict[yearlyItemsGrowth.year] = yearlyItemsGrowth.value
            yearIs = 'key'
            requestFrom = 'keyRatioIndusSpecific'
            processedGrowthData = processDictForGrowthFormula(growthGraphDict, yearIs, requestFrom)
            growthData = calculateProgrammedGrowth(processedGrowthData)
            graphDict['growth'] = growthData
        else:
            graphDict['type'] = 'Percentage'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
        graphDict['data'] = dataDict
        graphDict['id'] = graph.id
        graphDict['description'] = graph.graphDescription
        indusGraphDict[graph.graphFor] = graphDict
    processedDeRatio = sortingDictLowToHigh(deRatio)
    processedCurrentRatio = sortingDictLowToHigh(currentRatio)
    processedQuickRatio = sortingDictLowToHigh(quickRatio)
    bookValues = {}
    bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    for item in bookValuesObjs:
        try:
            totalShareOutStandValueObj = stockBalanceSheet.objects.get(stockProfileName=stock, year=item.year)
            totalShareOutstanding = totalShareOutStandValueObj.totalCommonSharesOutstanding
            newBookValue = item.bookValue / totalShareOutstanding
            bookValues[item.year] = newBookValue
        except:
            pass
    bookValuestoEdit = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    bookValuestoEdit_list = []
    try:
        if bookValuestoEdit:
            for each in bookValuestoEdit:
                bookValuestoEdit_ser = bookValueDataSerializer(each)
                bookValuestoEdit_list.append(bookValuestoEdit_ser.data)
    except:
        bookValuestoEdit = None
        bookValuestoEdit_list = []

    # createBookValue = bookValueDataForm()
    #
    try:
        valuationRatioInst = valuationRatio.objects.latest('id')
        if valuationRatioInst:
            valuationRatioInst_details = valuationRatioSerializer(valuationRatioInst)
            valuationRatioInst_details = valuationRatioInst_details.data
    except:
        valuationRatioInst = None
        valuationRatioInst_details = ""
    valuationRatioInstForm = valuationRatioForm(instance=valuationRatioInst)
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
        if iDescriptionForKeyRatiosInst:
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosSerializer(iDescriptionForKeyRatiosInst)
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosInst_details.data
    except:
        iDescriptionForKeyRatiosInst = None
        iDescriptionForKeyRatiosInst_details = ""
    try:
        financialFigureUnitsInst = financialFigureUnits.objects.get(stockProfileName=stock)
    except:
        financialFigureUnitsInst = None

    response_dict = {}
    stock_detail = {}
    stock_detail['extraData'] = {}
    if stock.seoTitle:
        stock_detail['extraData']['seoTitle'] = stock.seoTitle
    if stock.stockName:
        stock_detail['extraData']['stockName'] = stock.stockName
    if stockGrowthInst_detail:
        stock_detail['extraData']['stockGrowthInst'] = stockGrowthInst_detail
    if stockSolvencyInst_detail:
        stock_detail['extraData']['stockSolvencyInst'] = stockSolvencyInst_detail
    if stockOperatingEfficiencyInst_detail:
        stock_detail['extraData']['stockOperatingEfficiencyInst'] = stockOperatingEfficiencyInst_detail
    if sectorSpecificRatiosInst_detail:
        stock_detail['extraData']['sectorSpecificRatiosInst'] = sectorSpecificRatiosInst_detail
    if stockRatiosInst_detail:
        stock_detail['extraData']['stockRatiosInst'] = stockRatiosInst_detail
    # stock_detail['id'] = Stock_id
    stock_detail['growth'] = {'label': 'Growth', 'data': {}, 'description': stockGrowthInst.description, 'child': {}}
    if stockProfitLoss_list and stockProfitLoss_list != []:
        stock_detail['growth']['child']['revenueGrowth'] = {'label': 'Revenue Growth', 'data': {},
                                                            'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                            'description': stockGrowthInst.revenueGrowthDescription,
                                                            'child': {}}
        revenueGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['revenue'] = item['totalRevenue']
            revenueGrowth_list.append(tmp)
        stock_detail['growth']['child']['revenueGrowth']['data']['revenueGrowth'] = revenueGrowth_list
        stock_detail['growth']['child']['revenueGrowth']['data'][
            'processedRevenueGrowthTextual'] = processedRevenueGrowthTextual

        stock_detail['growth']['child']['netProfitGrowth'] = {'label': 'Net Profit Growth', 'data': {},
                                                              'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                              'description': stockGrowthInst.netProfitGrowthPATDescription,
                                                              'child': {}}
        netProfitGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['netIncome'] = item['netIncome']
            netProfitGrowth_list.append(tmp)
        stock_detail['growth']['child']['netProfitGrowth']['data']['netProfitGrowth'] = netProfitGrowth_list
        stock_detail['growth']['child']['netProfitGrowth']['data'][
            'processedNetProfitGrowthTextual'] = processedNetProfitGrowthTextual

        stock_detail['growth']['child']['EPSGrowth'] = {'label': 'EPS Growth', 'data': {}, 'value_in': '₹',
                                                        'description': stockGrowthInst.EPSGrowthDescription,
                                                        'child': {}}
        EPSGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['basicEPS'] = item['basicEPS']
            EPSGrowth_list.append(tmp)
        stock_detail['growth']['child']['EPSGrowth']['data']['EPSGrowth'] = EPSGrowth_list
        stock_detail['growth']['child']['EPSGrowth']['data']['processedEPSGrowthTextual'] = processedEPSGrowthTextual

    if bookValues and bookValues != {}:
        stock_detail['growth']['child']['bookValueGrowth'] = {'label': 'Book Value Growth',
                                                              'data': {'bookValues': bookValues,
                                                                       'processedBookValueGrowthTextual': processedBookValueGrowthTextual},
                                                              'value_in': '₹',
                                                              'description': stockGrowthInst.bookValueGrowthDescription,
                                                              'child': {}}
    # stock_detail['growth']['child']['bookValueGrowth']['data'] = bookValues

    if stockProfitLoss_list and stockProfitLoss_list != []:
        stock_detail['growth']['child']['ebidtaGrowth'] = {'label': 'EBIDTA Growth', 'data': {},
                                                           'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                           'description': stockGrowthInst.EBIDTAGrowthDescription,
                                                           'child': {}}
        ebidtaGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['ebidta'] = item['ebidta']
            ebidtaGrowth_list.append(tmp)
        stock_detail['growth']['child']['ebidtaGrowth']['data']['ebidtaGrowth'] = ebidtaGrowth_list
        stock_detail['growth']['child']['ebidtaGrowth']['data'][
            'processedEBITDAGrowthTextual'] = processedEBITDAGrowthTextual

        stock_detail['growth']['child']['operatingProfitGrowth'] = {'label': 'Operating Profit Growth', 'data': {},
                                                                    'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                                    'description': stockGrowthInst.operatingProfitGrowthDescription,
                                                                    'child': {}}
        operatingProfitGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['pbit'] = item['pbit']
            operatingProfitGrowth_list.append(tmp)
        stock_detail['growth']['child']['operatingProfitGrowth']['data'][
            'operatingProfitGrowth'] = operatingProfitGrowth_list
        stock_detail['growth']['child']['operatingProfitGrowth']['data'][
            'processedGrowthData'] = processedPBITGrowthTextual

    if stockBalanceSheet_list and stockBalanceSheet_list != []:
        stock_detail['growth']['child']['assetGrowth'] = {'label': 'Asset Growth', 'data': {},
                                                          'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                          'description': stockGrowthInst.assestsGrowthDescription,
                                                          'child': {}}
        assetGrowth_list = []
        for item in stockBalanceSheet_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['totalAssets'] = item['totalAssets']
            assetGrowth_list.append(tmp)
        stock_detail['growth']['child']['assetGrowth']['data']['assetGrowth'] = assetGrowth_list
        stock_detail['growth']['child']['assetGrowth']['data'][
            'processedAssetGrowthTextual'] = processedAssetGrowthTextual

    if stockCashFlow_list and stockCashFlow_list != []:
        stock_detail['growth']['child']['cashFlowFromFinancing'] = {'label': 'Cashflow from Financing', 'data': {},
                                                                    'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                                    'description': stockGrowthInst.cashFlowFromFinancingDescription,
                                                                    'child': {}}
        cashFlowFromFinancing_list = []
        for item in stockCashFlow_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['cashFromFinancingActivities'] = item['cashFromFinancingActivities']
            cashFlowFromFinancing_list.append(tmp)
        stock_detail['growth']['child']['cashFlowFromFinancing']['data'][
            'cashFlowFromFinancing'] = cashFlowFromFinancing_list
        stock_detail['growth']['child']['cashFlowFromFinancing']['data'][
            'processedCashFlowGrowthFinancingTextual'] = processedCashFlowGrowthFinancingTextual

        stock_detail['growth']['child']['cashFlowFromOperating'] = {'label': 'Cashflow from Operating', 'data': {},
                                                                    'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                                    'description': stockGrowthInst.cashFlowFromOperationsDescription,
                                                                    'child': {}}
        cashFlowFromOperating_list = []
        for item in stockCashFlow_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['cashFromOperatingActivities'] = item['cashFromOperatingActivities']
            cashFlowFromOperating_list.append(tmp)
        stock_detail['growth']['child']['cashFlowFromOperating']['data'][
            'cashFlowFromOperating'] = cashFlowFromOperating_list
        stock_detail['growth']['child']['cashFlowFromOperating']['data'][
            'processedCashFlowGrowthTextual'] = processedCashFlowGrowthTextual

    if stock_detail['growth']['data'] == {} and stock_detail['growth']['child'] == {}:
        stock_detail.pop('growth')

    stock_detail['solvencyRatios'] = {'label': 'Solvency Ratios', 'data': {},
                                      'description': stockSolvencyInst.solvencyDescription, 'child': {}}
    if processedDeRatio and processedDeRatio != {}:
        stock_detail['solvencyRatios']['child']['DERatio'] = {'label': 'DE Ratio', 'data': processedDeRatio,
                                                              'description': stockSolvencyInst.DERatioDescription,
                                                              'child': {}}
    if processedCurrentRatio and processedCurrentRatio != {}:
        stock_detail['solvencyRatios']['child']['currentRatio'] = {'label': 'Current Ratio',
                                                                   'description': stockSolvencyInst.currentRatioDescription,
                                                                   'data': processedCurrentRatio, 'child': {}}
    if processedQuickRatio and processedQuickRatio != {}:
        stock_detail['solvencyRatios']['child']['quickRatio'] = {'label': 'Quick Ratio', 'data': processedQuickRatio,
                                                                 'description': stockSolvencyInst.quickRatioDescription,
                                                                 'child': {}}
    if interestCoverageRatio and interestCoverageRatio != {}:
        del interestCoverageRatio[list(interestCoverageRatio)[0]]
        stock_detail['solvencyRatios']['child']['interestCoverageRatio'] = {'label': 'Interest Coverage Ratio',
                                                                            'description': stockSolvencyInst.interestCoverageRatioDescription,
                                                                            'data': interestCoverageRatio, 'child': {}}

    if stock_detail['solvencyRatios']['data'] == {} and stock_detail['solvencyRatios']['child'] == {}:
        stock_detail.pop('solvencyRatios')

    stock_detail['sectorSpecificRatios'] = {'label': 'Sector Specific Ratios', 'data': {}, 'child': {}}
    for item in indusGraphDict:
        stock_detail['sectorSpecificRatios']['child'][item] = indusGraphDict[item]
        stock_detail['sectorSpecificRatios']['child'][item]['label'] = str(item)
        stock_detail['sectorSpecificRatios']['child'][item]['child'] = {}
    if stock_detail['sectorSpecificRatios']['data'] == {} and stock_detail['sectorSpecificRatios']['child'] == {}:
        stock_detail.pop('sectorSpecificRatios')

    stock_detail['operatingEfficiency'] = {'label': 'Operating Efficiency', 'data': {},
                                           'description': stockOperatingEfficiencyInst.operatingEfficiencyDescription,
                                           'child': {}}
    if operatingProfitEBITmargin and operatingProfitEBITmargin != {}:
        stock_detail['operatingEfficiency']['child']['operatingProfitEBITMargin'] = {
            'label': 'Operating Profit EBIT Margin', 'data': operatingProfitEBITmargin,
            'description': stockOperatingEfficiencyInst.operatingProfitEBITMarginDescription, 'child': {}}
    if pbtMargin and pbtMargin != {}:
        stock_detail['operatingEfficiency']['child']['profitBeforeTaxMargin'] = {'label': 'Profit before Tax Margin',
                                                                                 'data': pbtMargin, 'value_in': '%',
                                                                                 'description': stockOperatingEfficiencyInst.PBTMarginDescription,
                                                                                 'child': {}}
    if patMargin and patMargin != {}:
        stock_detail['operatingEfficiency']['child']['profitAfterTaxMargin'] = {'label': 'Profit after Tax Margin',
                                                                                'data': patMargin, 'value_in': '%',
                                                                                'description': stockOperatingEfficiencyInst.PATMarginDescription,
                                                                                'child': {}}

    if stock_detail['operatingEfficiency']['data'] == {} and stock_detail['operatingEfficiency']['child'] == {}:
        stock_detail.pop('operatingEfficiency')

    stock_detail['profitablityRatio'] = {'label': 'Profitablity Ratio', 'data': {},
                                         'description': stockRatiosInst.profitiabilityDescription, 'child': {}}
    if returnOnEquity and returnOnEquity != {}:
        del returnOnEquity[list(returnOnEquity)[0]]
        stock_detail['profitablityRatio']['child']['returnOnEquity'] = {'label': 'Return on Equity',
                                                                        'data': returnOnEquity, 'value_in': '%',
                                                                        'description': stockRatiosInst.returnOnEquityDescription,
                                                                        'child': {}}
    if roce and roce != {}:
        del roce[list(roce)[0]]
        stock_detail['profitablityRatio']['child']['roce'] = {'label': 'ROCE', 'data': roce, 'value_in': '%',
                                                              'description': stockRatiosInst.ROCEDescription,
                                                              'child': {}}
    if returnOnAssets and returnOnAssets != {}:
        del returnOnAssets[list(returnOnAssets)[0]]
        stock_detail['profitablityRatio']['child']['returnOnAssests'] = {'label': 'Return on Assets',
                                                                         'data': returnOnAssets, 'value_in': '%',
                                                                         'description': stockRatiosInst.returnOnAssestsDescription,
                                                                         'child': {}}

    if stock_detail['profitablityRatio']['data'] == {} and stock_detail['profitablityRatio']['child'] == {}:
        stock_detail.pop('profitablityRatio')

    stock_detail['valuationRatios'] = {'label': 'Valuation Ratios', 'data': {},
                                       'description': valuationRatioInst.valuationRatioDescription, 'child': {}}
    if dividentYield and dividentYield != {}:
        stock_detail['valuationRatios']['child']['dividendYield'] = {'data': dividentYield, 'label': 'Dividend Yield',
                                                                     'child': {}, 'value_in': '%',
                                                                     'description': valuationRatioInst.valuationRatioDividendYield}

    if earningYield and earningYield != {}:
        del earningYield[list(earningYield)[0]]
        stock_detail['valuationRatios']['child']['earningYield'] = {'data': earningYield, 'value_in': '%','child' : {},
                                                                   'description': valuationRatioInst.valuationRatioEarningYield}
    if bookValues and bookValues != {}:
        stock_detail['valuationRatios']['data']['Price/bookValues'] = bookValues
    # stock_detail['valuationRatios']['data']['Price/Earning'] = {'label': 'Price/Earning','data': {}, 'child':{}}
    # stock_detail['valuationRatios']['data']['EV/EBITDA'] = {'label': 'EV/EBITDA','data': {}, 'child':{}}
    # stock_detail['valuationRatios']['data']['MarketCapital/Sales'] = {'label': 'Market Capital/Sales','data': {}, 'child':{}}
    if stock_detail['valuationRatios']['data'] == {} and stock_detail['valuationRatios']['child'] == {}:
        stock_detail.pop('valuationRatios')

    response_dict.update({"stock": stock_detail})

    return Response({'response': response_dict})


#
@api_view(['GET'])
def getKeyRatioForBankNBFCsView_01(request, slug):
    stock_detail = ""
    response_dict = {}
    stock = get_object_or_404(stockBasicDetail, id=slug)
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
        # Stock_id  = stock_detail['id']
    stockProfitLoss_list = []
    stockProfitLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if stockProfitLoss:
            for each in stockProfitLoss:
                stockProfitLoss_ser = stockProfitAndLossBankNBFCSerializer(each)
                stockProfitLoss_list.append(stockProfitLoss_ser.data)
    except:
        stockProfitLoss = None
        stockProfitLoss_list = []

    stockBalanceSheet_list = []
    balanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if balanceSheet:
            for each in balanceSheet:
                stockBalanceSheet_ser = stockBalanceSheetBankNBFCSerializer(each)
                stockBalanceSheet_list.append(stockBalanceSheet_ser.data)
    except:
        balanceSheet = None
        stockBalanceSheet_list = []
    stockCashFlow_list = []
    cashFlow = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    try:
        if cashFlow:
            for each in cashFlow:
                stockCashFlow_ser = stockCashFlowSerializer(each)
                stockCashFlow_list.append(stockCashFlow_ser.data)
    except:
        cashFlow = None
        stockCashFlow_list = []
    # Required changes in formuals Calculation starts - done
    deRatio, currentRatio, quickRatio, averageTotalEquityDict, avgTotalLongTermDebtDict, avgTotalAssetDict, avgROceDenoPart = stockBalanceSheetCalculationForBankNBFc(
        stock)
    interestCoverageRatio, operatingProfitEBITmargin, pbtMargin, patMargin, netIncomeDict, pbitDict = stockProfitAndLossCalculationForBankNBFc(
        stock)
    # Required changes in formuals Calculation ends - done
    returnOnEquity = {}
    roce = {}
    returnOnAssets = {}
    dividentYield = {}
    earningYield = {}
    for key, val in netIncomeDict.items():
        val2 = averageTotalEquityDict.get(key)
        if val2:
            valEquity = val2
        else:
            valEquity = 1
        catROERounded = round((val / valEquity) * 100, 2)
        returnOnEquity[key] = catROERounded
    for item in stockProfitLoss:
        # try:
        #         currentStockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
        #         currentStockPrice = currentStockPriceInst.investorPrice
        # except:
        #         currentStockPrice = 0
        currentStockPrice = localOrScreenerPriceView(stock)
        # divident
        try:
            DPSforThisYear = item.DPS
        except:
            DPSforThisYear = None
        calDividentforThisYear = dividentYieldGraphView(DPSforThisYear, currentStockPrice)
        if calDividentforThisYear:
            dividentYield[item.year] = calDividentforThisYear
        # earning
        calEPSforThisYear = check_eps_basic_or_diluted(item.basicEPS, item.dilutedEPS)
        calEarningforThisYear = earningYieldGraphView(calEPSforThisYear, currentStockPrice)
        if calEarningforThisYear:
            earningYield[item.year] = calEarningforThisYear
    # Ishima remove ROCE  starts
    # for key, val in pbitDict.items():
    #         val2 = avgTotalAssetDict.get(key)
    #         val3 = avgROceDenoPart.get(key)
    #         avgROceDenoPart
    #         if val2:
    #                 valAverageAsset = val2
    #         else :
    #                 valAverageAsset = 0

    #         if val3:
    #                 valCurrentLiab = val3
    #         else :
    #                 valCurrentLiab = 0

    #         sumofAssestAndCrrLiabilities = valAverageAsset - valCurrentLiab
    #         if not sumofAssestAndCrrLiabilities:
    #                 sumofAssestAndCrrLiabilities = 1
    #         roce[key] = round((val / ( sumofAssestAndCrrLiabilities )) * 100,2)
    # Ishima aksed to remove ROCE ends
    for key, val in netIncomeDict.items():
        val2 = avgTotalAssetDict.get(key)
        # val3 = avgIntangibleAssetDict.get(key)
        if val2:
            valAverageAsset = val2
        else:
            valAverageAsset = 0
        # if val3:
        #         valAverageIntangibleAsset = val3
        # else :
        #         valAverageIntangibleAsset = 0
        # processedVal = valAverageAsset - valAverageIntangibleAsset
        # changes from Kulmehar starts
        processedVal = valAverageAsset
        # chnages from Kulmehar ends
        if processedVal == 0:
            processedVal = 1
        returnOnAssets[key] = round((val / processedVal) * 100, 2)

    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
            stockAdmInst_detail = stockAdmInst_detail.data
        # print("stockAdmInst", stockAdmInst)
    except:
        stockAdmInst = None
        stockAdmInst_detail = ""

    stockGrowthInst_detail = ""
    try:
        stockGrowthInst = stockGrowth.objects.get(stockProfileName=stock)
        if stockGrowthInst:
            stockGrowthInst_detail = stockGrowthSerializer(stockGrowthInst)
            stockGrowthInst_detail = stockGrowthInst_detail.data
        # print("stockGrowthInst", stockGrowthInst)
    except:
        stockGrowthInst = None
        stockGrowthInst_detail = ""
    # createStockGrowth = stockGrowthForm(instance=stockGrowthInst)
    stockSolvencyInst_detail = ""
    try:
        stockSolvencyInst = stockSolvency.objects.get(stockProfileName=stock)
        if stockSolvencyInst:
            stockSolvencyInst_detail = stockSolvencySerializer(stockSolvencyInst)
            stockSolvencyInst_detail = stockSolvencyInst_detail.data
        # print("stockSolvencyInst", stockSolvencyInst)
    except:
        stockSolvencyInst = None
        stockSolvencyInst_detail = ""
    # createStockSolvency = stockSolvencyForm(instance=stockSolvencyInst)
    stockOperatingEfficiencyInst_detail = ""
    try:
        stockOperatingEfficiencyInst = stockOperatingEfficiency.objects.get(stockProfileName=stock)
        if stockOperatingEfficiencyInst:
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencySerializer(stockOperatingEfficiencyInst)
            stockOperatingEfficiencyInst_detail = stockOperatingEfficiencyInst_detail.data
        # print("stockOperatingEfficiencyInst", stockOperatingEfficiencyInst)
    except:
        stockOperatingEfficiencyInst = None
        stockOperatingEfficiencyInst_detail = ""
    # createStockOperatingEfficiency = stockOperatingEfficiencyForm(instance=stockOperatingEfficiencyInst)
    sectorSpecificRatiosInst_detail = ""
    try:
        sectorSpecificRatiosInst = sectorSpecificRatios.objects.get(stockProfileName=stock)
        if sectorSpecificRatiosInst:
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosSerializer(sectorSpecificRatiosInst)
            sectorSpecificRatiosInst_detail = sectorSpecificRatiosInst_detail.data
        # print('sectorSpecificRatiosInst', sectorSpecificRatiosInst)
    except:
        sectorSpecificRatiosInst = None
        sectorSpecificRatiosInst_detail = ""
    # createSectorSpecificRatios = sectorSpecificRatiosForm(instance=sectorSpecificRatiosInst)
    stockRatiosInst_detail = ""
    try:
        stockRatiosInst = stockRatios.objects.get(stockProfileName=stock)
        if stockRatiosInst:
            stockRatiosInst_detail = stockRatiosSerializer(stockRatiosInst)
            stockRatiosInst_detail = stockRatiosInst_detail.data
        # print('stockRatiosInst', stockRatiosInst)
    except:
        stockRatiosInst = None
        stockRatiosInst_detail = ""
    despositoryOptions, saleType = rightSideMenuObjs()
    # createStockRatios = stockRatiosForm(instance=stockRatiosInst)
    stockTransferDepositoryOptions_list = []
    try:
        if despositoryOptions:
            for each in despositoryOptions:
                stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
    except:
        despositoryOptions = None
        stockTransferDepositoryOptions_list = []
    saleTypeOptions_list = []
    try:
        if saleType:
            for each in saleType:
                saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                saleTypeOptions_list.append(saleTypeOptions_ser.data)
    except:
        saleType = None
        saleTypeOptions_list = []
    # Required changes in formuals Calculation starts - done
    returnedGrowthDataRevenue, returnedRevenueGrowthAlgoProgrammedData, returnedNetProfitGrowthData, returnedNetProfitAlgoProgrammedData, returnedEPSGrowthData, returnedEPSAlgoProgrammedData, returnedEBITDAGrowthData, returnedEBITDAAlgoProgrammedData, returnedPBITGrowthData, returnedPBITAlgoProgrammedData = calGrowthTemplateDataViewFrBankNBFcs(
        stock)

    processedRevenueGrowthTextual = calculateProgrammedGrowth(returnedRevenueGrowthAlgoProgrammedData)
    processedNetProfitGrowthTextual = calculateProgrammedGrowth(returnedNetProfitAlgoProgrammedData)
    processedEPSGrowthTextual = calculateProgrammedGrowth(returnedEPSAlgoProgrammedData)
    processedEBITDAGrowthTextual = calculateProgrammedGrowth(returnedEBITDAAlgoProgrammedData)
    processedPBITGrowthTextual = calculateProgrammedGrowth(returnedPBITAlgoProgrammedData)

    processedBookValueGrowthTextual = growthCalculatorForAnnualValuesFrBankNBFCs(stock, growthFor='bookValue')
    processedAssetGrowthTextual = growthCalculatorForAnnualValuesFrBankNBFCs(stock, growthFor='assetGrowth')
    processedCashFlowGrowthTextual, processedCashFlowGrowthFinancingTextual = growthCalculatorForAnnualValuesFrBankNBFCs(
        stock, growthFor='cashFlow')
    # Required changes in formuals Calculation ends - done
    indusSpecificGraphs = industrySpecificGraphs.objects.filter(stockProfileName=stock)
    industrySpecificGraph = industrySpecificGraphForm()
    industrySpecificValsGraph = industrySpecificGraphValsForm()
    indusGraphDict = {}
    for graph in indusSpecificGraphs:
        indusSpecificValsGraphs = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by('year')[0:10]
        indusSpecificValsGraphsForGrowth = industrySpecificGraphsValues.objects.filter(valuesFor=graph).order_by(
            '-year')[0:10]
        graphDict = {}
        dataDict = {}
        growthGraphDict = {}
        forCount = 0
        if graph.graphType == 'Value':
            graphDict['type'] = 'Value'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                forCount += 1
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
            for yearlyItemsGrowth in indusSpecificValsGraphsForGrowth:
                growthGraphDict[yearlyItemsGrowth.year] = yearlyItemsGrowth.value
            yearIs = 'key'
            requestFrom = 'keyRatioIndusSpecific'
            processedGrowthData = processDictForGrowthFormula(growthGraphDict, yearIs, requestFrom)
            growthData = calculateProgrammedGrowth(processedGrowthData)
            graphDict['growth'] = growthData
        else:
            graphDict['type'] = 'Percentage'
            for yearlyItems in indusSpecificValsGraphs:
                annualData = {}
                annualData['id'] = yearlyItems.id
                annualData['value'] = yearlyItems.value
                dataDict[yearlyItems.year] = annualData
        graphDict['data'] = dataDict
        graphDict['id'] = graph.id
        graphDict['description'] = graph.graphDescription
        graphDict['valueFori'] = graph.iDescription
        indusGraphDict[graph.graphFor] = graphDict
    processedDeRatio = sortingDictLowToHigh(deRatio)
    processedCurrentRatio = sortingDictLowToHigh(currentRatio)
    processedQuickRatio = sortingDictLowToHigh(quickRatio)
    bookValues = {}
    bookValuesObjs = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    for item in bookValuesObjs:
        try:
            totalShareOutStandValueObj = stockBalanceSheetBankNBFC.objects.get(stockProfileName=stock, year=item.year)
            totalShareOutstanding = totalShareOutStandValueObj.totalCommonSharesOutstanding
            newBookValue = item.bookValue / totalShareOutstanding
            bookValues[item.year] = newBookValue
        except:
            pass
    bookValuestoEdit = bookValueData.objects.filter(stockProfileName=stock).order_by('year')[0:10]
    bookValuestoEdit_list = []
    try:
        if bookValuestoEdit:
            for each in bookValuestoEdit:
                bookValuestoEdit_ser = bookValueDataSerializer(each)
                bookValuestoEdit_list.append(bookValuestoEdit_ser.data)
    except:
        bookValuestoEdit = None
        bookValuestoEdit_list = []
    # createBookValue = bookValueDataForm()
    tier1CapitalRatioDict = {}
    tier2CapitalRatioDict = {}
    tangibleBookVaueDict = {}
    aumDict = {}
    aumGrowthDict = {}
    for item in balanceSheet:
        if item.tier1CapitalRatio:
            tier1CapitalRatioDict[item.year] = item.tier1CapitalRatio
        if item.tier2CapitalRatio:
            tier2CapitalRatioDict[item.year] = item.tier2CapitalRatio
        if item.tangibleBookValue:
            tangibleBookVaueDict[item.year] = item.tangibleBookValue
        if item.aum:
            aumDict[item.year] = item.aum
        if item.aumGrowth:
            aumGrowthDict[item.year] = item.aumGrowth
    #
    try:
        valuationRatioInst = valuationRatio.objects.latest('id')
        if valuationRatioInst:
            valuationRatioInst_details = valuationRatioSerializer(valuationRatioInst)
            valuationRatioInst_details = valuationRatioInst_details.data
    except:
        valuationRatioInst = None
        valuationRatioInst_details = ""
    # valuationRatioInstForm = valuationRatioForm(instance=valuationRatioInst)
    try:
        iDescriptionForKeyRatiosInst = iDescriptionForKeyRatios.objects.latest('id')
        if iDescriptionForKeyRatiosInst:
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosSerializer(iDescriptionForKeyRatiosInst)
            iDescriptionForKeyRatiosInst_details = iDescriptionForKeyRatiosInst_details.data
    except:
        iDescriptionForKeyRatiosInst = None
        iDescriptionForKeyRatiosInst_details = ""
    #
    bankNBFCRatioDescriptionInst_detail = ""
    try:
        # bankNBFCRatioDescriptionInst = bankNBFCRatioDescription.objects.latest('id')
        bankNBFCRatioDescriptionInst = bankNBFCRatioDescription.objects.get(stockProfileName=stock)
        if bankNBFCRatioDescriptionInst:
            bankNBFCRatioDescriptionInst_detail = bankNBFCRatioDescriptionSerializer(bankNBFCRatioDescriptionInst)
            bankNBFCRatioDescriptionInst_detail = bankNBFCRatioDescriptionInst_detail.data
    except:
        bankNBFCRatioDescriptionInst = None
        bankNBFCRatioDescriptionInst_detail = ""
    # bankNBFCRatioDescriptionInstForm = bankNBFCRatioDescriptionForm(instance=bankNBFCRatioDescriptionInst)
    RBIStandardVals = valuesRBIStandards.objects.all().order_by('year')
    RBIStandardVals_list = []
    try:
        if RBIStandardVals:
            for each in RBIStandardVals:
                RBIStandardVals_ser = valuesRBIStandardsSerializer(each)
                RBIStandardVals_list.append(RBIStandardVals_ser.data)
    except:
        RBIStandardVals_list = []
    companyForRBIVals = companyRatios.objects.filter(stockProfileName=stock).order_by('year')
    companyForRBIVals_list = []
    try:
        if companyForRBIVals:
            for each in companyForRBIVals:
                companyForRBIVals_ser = companyRatiosSerializer(each)
                companyForRBIVals_list.append(companyForRBIVals_ser.data)
    except:
        companyForRBIVals_list = []
    RBIGraphDict = {}
    commonRBIStockYearList = []
    for item in companyForRBIVals:
        if item.year:
            if RBIStandardVals.filter(year=item.year).exists():
                commonRBIStockYearList.append(item.year)
    tempDict = {}
    RBICompChart1 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart1 = True
        if RBIData.RBI_CARValue and stockData.carValue:
            tempList.append(RBIData.RBI_CARValue)
            tempList.append(stockData.carValue)
            tempDict[item] = tempList
    RBIGraphDict['CAR'] = tempDict
    tempDict = {}
    RBICompChart2 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart2 = True
        if RBIData.RBI_tier1Value and stockData.tier1Value:
            tempList.append(RBIData.RBI_tier1Value)
            tempList.append(stockData.tier1Value)
            tempDict[item] = tempList
    RBIGraphDict['tier1'] = tempDict
    tempDict = {}
    RBICompChart3 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart3 = True
        if RBIData.RBI_tier2Value and stockData.tier2Value:
            tempList.append(RBIData.RBI_tier2Value)
            tempList.append(stockData.tier2Value)
            tempDict[item] = tempList
    RBIGraphDict['tier2'] = tempDict
    tempDict = {}
    RBICompChart4 = False
    for item in commonRBIStockYearList:
        RBIData = RBIStandardVals.get(year=item)
        stockData = companyForRBIVals.get(year=item)
        tempList = []
        RBICompChart4 = True
        if RBIData.RBI_maintenanceMarginRequirement and stockData.maintenanceMarginRequirement:
            tempList.append(RBIData.RBI_maintenanceMarginRequirement)
            tempList.append(stockData.maintenanceMarginRequirement)
            tempDict[item] = tempList
    RBIGraphDict['MMR'] = tempDict
    # companyRatioCreateForm = companyRatiosForm()
    regulatoryRatiosInst_detail = ""
    try:
        regulatoryRatiosInst = regulatoryRatios.objects.get(stockProfileName=stock)
        if regulatoryRatiosInst:
            regulatoryRatiosInst_detail = regulatoryRatiosSerializer(regulatoryRatiosInst)
            regulatoryRatiosInst_detail = regulatoryRatiosInst_detail.data
    except:
        regulatoryRatiosInst = None
        regulatoryRatiosInst_detail = ""
    # regulatoryRatiosInstForm = regulatoryRatiosForm(instance=regulatoryRatiosInst)
    try:
        financialFigureUnitsInst = financialFigureUnits.objects.get(stockProfileName=stock)
    except:
        financialFigureUnitsInst = None

    response_dict = {}
    stock_detail = {}
    stock_detail['extraData'] = {}
    if stock.seoTitle:
        stock_detail['extraData']['seoTitle'] = stock.seoTitle
    if stock.stockName:
        stock_detail['extraData']['stockName'] = stock.stockName
    if stockGrowthInst_detail:
        stock_detail['extraData']['stockGrowthInst'] = stockGrowthInst_detail
    if stockSolvencyInst_detail:
        stock_detail['extraData']['stockSolvencyInst'] = stockSolvencyInst_detail
    if stockOperatingEfficiencyInst_detail:
        stock_detail['extraData']['stockOperatingEfficiencyInst'] = stockOperatingEfficiencyInst_detail
    if sectorSpecificRatiosInst_detail:
        stock_detail['extraData']['sectorSpecificRatiosInst'] = sectorSpecificRatiosInst_detail
    if stockRatiosInst_detail:
        stock_detail['extraData']['stockRatiosInst'] = stockRatiosInst_detail
    # stock_detail['id'] = Stock_id
    stock_detail['growth'] = {'label': 'Growth', 'data': {}, 'description': stockGrowthInst.description, 'child': {}}
    if stockProfitLoss_list and stockProfitLoss_list != []:
        stock_detail['growth']['child']['revenueGrowth'] = {'label': 'Revenue Growth', 'data': {},
                                                            'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                            'description': stockGrowthInst.revenueGrowthDescription,
                                                            'child': {}}
        revenueGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['revenue'] = item['totalRevenue']
            revenueGrowth_list.append(tmp)
        stock_detail['growth']['child']['revenueGrowth']['data']['revenueGrowth'] = revenueGrowth_list
        stock_detail['growth']['child']['revenueGrowth']['data'][
            'processedRevenueGrowthTextual'] = processedRevenueGrowthTextual

        stock_detail['growth']['child']['netProfitGrowth'] = {'label': 'Net Profit Growth', 'data': {},
                                                              'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                              'description': stockGrowthInst.netProfitGrowthPATDescription,
                                                              'child': {}}
        netProfitGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['netIncome'] = item['netIncome']
            netProfitGrowth_list.append(tmp)
        stock_detail['growth']['child']['netProfitGrowth']['data']['netProfitGrowth'] = netProfitGrowth_list
        stock_detail['growth']['child']['netProfitGrowth']['data'][
            'processedNetProfitGrowthTextual'] = processedNetProfitGrowthTextual

        stock_detail['growth']['child']['EPSGrowth'] = {'label': 'EPS Growth', 'data': {}, 'value_in': '₹',
                                                        'description': stockGrowthInst.EPSGrowthDescription,
                                                        'child': {}}
        EPSGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['basicEPS'] = item['basicEPS']
            EPSGrowth_list.append(tmp)
        stock_detail['growth']['child']['EPSGrowth']['data']['EPSGrowth'] = EPSGrowth_list
        stock_detail['growth']['child']['EPSGrowth']['data']['processedEPSGrowthTextual'] = processedEPSGrowthTextual

    if bookValues and bookValues != {}:
        stock_detail['growth']['child']['bookValueGrowth'] = {'label': 'Book Value Growth',
                                                              'data': {'bookValues': bookValues,
                                                                       'processedBookValueGrowthTextual': processedBookValueGrowthTextual},
                                                              'value_in': '₹',
                                                              'description': stockGrowthInst.bookValueGrowthDescription,
                                                              'child': {}}
    # stock_detail['growth']['child']['bookValueGrowth']['data'] = bookValues

    if stockProfitLoss_list and stockProfitLoss_list != []:
        stock_detail['growth']['child']['ebidtaGrowth'] = {'label': 'EBIDTA Growth', 'data': {},
                                                           'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                           'description': stockGrowthInst.EBIDTAGrowthDescription,
                                                           'child': {}}
        ebidtaGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['ebidta'] = item['ebidta']
            ebidtaGrowth_list.append(tmp)
        stock_detail['growth']['child']['ebidtaGrowth']['data']['ebidtaGrowth'] = ebidtaGrowth_list
        stock_detail['growth']['child']['ebidtaGrowth']['data'][
            'processedEBITDAGrowthTextual'] = processedEBITDAGrowthTextual

        stock_detail['growth']['child']['operatingProfitGrowth'] = {'label': 'Operating Profit Growth', 'data': {},
                                                                    'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                                    'description': stockGrowthInst.operatingProfitGrowthDescription,
                                                                    'child': {}}
        operatingProfitGrowth_list = []
        for item in stockProfitLoss_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['pbit'] = item['pbit']
            operatingProfitGrowth_list.append(tmp)
        stock_detail['growth']['child']['operatingProfitGrowth']['data'][
            'operatingProfitGrowth'] = operatingProfitGrowth_list
        stock_detail['growth']['child']['operatingProfitGrowth']['data'][
            'processedGrowthData'] = processedPBITGrowthTextual

    if stockBalanceSheet_list and stockBalanceSheet_list != []:
        stock_detail['growth']['child']['assetGrowth'] = {'label': 'Asset Growth', 'data': {},
                                                          'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                          'description': stockGrowthInst.assestsGrowthDescription,
                                                          'child': {}}
        assetGrowth_list = []
        for item in stockBalanceSheet_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['totalAssets'] = item['totalAssets']
            assetGrowth_list.append(tmp)
        stock_detail['growth']['child']['assetGrowth']['data']['assetGrowth'] = assetGrowth_list
        stock_detail['growth']['child']['assetGrowth']['data'][
            'processedAssetGrowthTextual'] = processedAssetGrowthTextual

    if stockCashFlow_list and stockCashFlow_list != []:
        stock_detail['growth']['child']['cashFlowFromFinancing'] = {'label': 'Cashflow from Financing', 'data': {},
                                                                    'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                                    'description': stockGrowthInst.cashFlowFromFinancingDescription,
                                                                    'child': {}}
        cashFlowFromFinancing_list = []
        for item in stockCashFlow_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['cashFromFinancingActivities'] = item['cashFromFinancingActivities']
            cashFlowFromFinancing_list.append(tmp)
        stock_detail['growth']['child']['cashFlowFromFinancing']['data'][
            'cashFlowFromFinancing'] = cashFlowFromFinancing_list
        stock_detail['growth']['child']['cashFlowFromFinancing']['data'][
            'processedCashFlowGrowthFinancingTextual'] = processedCashFlowGrowthFinancingTextual

        stock_detail['growth']['child']['cashFlowFromOperating'] = {'label': 'Cashflow from Operating', 'data': {},
                                                                    'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                                    'description': stockGrowthInst.cashFlowFromOperationsDescription,
                                                                    'child': {}}
        cashFlowFromOperating_list = []
        for item in stockCashFlow_list:
            tmp = {}
            tmp['year'] = item['year']
            tmp['cashFromOperatingActivities'] = item['cashFromOperatingActivities']
            cashFlowFromOperating_list.append(tmp)
        stock_detail['growth']['child']['cashFlowFromOperating']['data'][
            'cashFlowFromOperating'] = cashFlowFromOperating_list
        stock_detail['growth']['child']['cashFlowFromOperating']['data'][
            'processedCashFlowGrowthTextual'] = processedCashFlowGrowthTextual

    if stock_detail['growth']['data'] == {} and stock_detail['growth']['child'] == {}:
        stock_detail.pop('growth')

    stock_detail['solvencyRatios'] = {'label': 'Solvency Ratios', 'data': {},
                                      'description': stockSolvencyInst.solvencyDescription, 'child': {}}
    if processedDeRatio and processedDeRatio != {}:
        stock_detail['solvencyRatios']['child']['DERatio'] = {'label': 'DE Ratio', 'data': processedDeRatio,
                                                              'description': stockSolvencyInst.DERatioDescription,
                                                              'child': {}}
    if processedCurrentRatio and processedCurrentRatio != {}:
        stock_detail['solvencyRatios']['child']['currentRatio'] = {'label': 'Current Ratio',
                                                                   'data': processedCurrentRatio,
                                                                   'description': stockSolvencyInst.currentRatioDescription,
                                                                   'child': {}}
    if processedQuickRatio and processedQuickRatio != {}:
        stock_detail['solvencyRatios']['child']['quickRatio'] = {'label': 'Quick Ratio', 'data': processedQuickRatio,
                                                                 'description': stockSolvencyInst.quickRatioDescription,
                                                                 'child': {}}
    if interestCoverageRatio and interestCoverageRatio != {}:
        del interestCoverageRatio[list(interestCoverageRatio)[0]]
        stock_detail['solvencyRatios']['child']['interestCoverageRatio'] = {'label': 'Interest Coverage Ratio',
                                                                            'data': interestCoverageRatio,
                                                                            'description': stockSolvencyInst.interestCoverageRatioDescription,
                                                                            'child': {}}

    if stock_detail['solvencyRatios']['data'] == {} and stock_detail['solvencyRatios']['child'] == {}:
        stock_detail.pop('solvencyRatios')
    stock_detail['sectorSpecificRatios'] = {'label': 'Sector Specific Ratios', 'data': {}, 'child': {}}
    for item in indusGraphDict:
        stock_detail['sectorSpecificRatios']['child'][item] = indusGraphDict[item]
        stock_detail['sectorSpecificRatios']['child'][item]['label'] = str(item)
        stock_detail['sectorSpecificRatios']['child'][item]['child'] = {}

    if stock_detail['sectorSpecificRatios']['data'] == {} and stock_detail['sectorSpecificRatios']['child'] == {}:
        stock_detail.pop('sectorSpecificRatios')
    # stock_detail['indusGraphDict'] = indusGraphDict
    stock_detail['operatingEfficiency'] = {'label': 'Operating Efficiency', 'data': {},
                                           'description': stockOperatingEfficiencyInst.operatingEfficiencyDescription,
                                           'child': {}}
    if operatingProfitEBITmargin and operatingProfitEBITmargin != {}:
        stock_detail['operatingEfficiency']['child']['operatingProfitEBITMargin'] = {
            'label': 'Operating Profit EBIT Margin', 'data': operatingProfitEBITmargin,
            'description': stockOperatingEfficiencyInst.operatingProfitEBITMarginDescription, 'child': {}}
    if pbtMargin and pbtMargin != {}:
        stock_detail['operatingEfficiency']['child']['profitBeforeTaxMargin'] = {'label': 'Profit before Tax Margin',
                                                                                 'data': pbtMargin, 'value_in': '%',
                                                                                 'description': stockOperatingEfficiencyInst.PBTMarginDescription,
                                                                                 'child': {}}
    if patMargin and patMargin != {}:
        stock_detail['operatingEfficiency']['child']['profitAfterTaxMargin'] = {'label': 'Profit after Tax Margin',
                                                                                'data': patMargin, 'value_in': '%',
                                                                                'description': stockOperatingEfficiencyInst.PATMarginDescription,
                                                                                'child': {}}

    if stock_detail['operatingEfficiency']['data'] == {} and stock_detail['operatingEfficiency']['child'] == {}:
        stock_detail.pop('operatingEfficiency')

    stock_detail['profitablityRatio'] = {'label': 'Profitablity Ratio', 'data': {},
                                         'description': stockRatiosInst.profitiabilityDescription, 'child': {}}
    if returnOnEquity and returnOnEquity != {}:
        del returnOnEquity[list(returnOnEquity)[0]]
        stock_detail['profitablityRatio']['child']['returnOnEquity'] = {'label': 'Return on Equity',
                                                                        'data': returnOnEquity, 'value_in': '%',
                                                                        'description': stockRatiosInst.returnOnEquityDescription,
                                                                        'child': {}}
    if roce and roce != {}:
        del roce[list(roce)[0]]
        stock_detail['profitablityRatio']['child']['roce'] = {'label': 'ROCE', 'data': roce, 'value_in': '%',
                                                              'description': stockRatiosInst.ROCEDescription,
                                                              'child': {}}
    if returnOnAssets and returnOnAssets != {}:
        del returnOnAssets[list(returnOnAssets)[0]]
        stock_detail['profitablityRatio']['child']['returnOnAssests'] = {'label': 'Return on Assets',
                                                                         'data': returnOnAssets, 'value_in': '%',
                                                                         'description': stockRatiosInst.returnOnAssestsDescription,
                                                                         'child': {}}

    if stock_detail['profitablityRatio']['data'] == {} and stock_detail['profitablityRatio']['child'] == {}:
        stock_detail.pop('profitablityRatio')

    stock_detail['valuationRatios'] = {'label': 'Valuation Ratios', 'data': {},
                                       'description': valuationRatioInst.valuationRatioDescription if valuationRatioInst else None,
                                       'child': {}}
    if dividentYield and dividentYield != {}:
        stock_detail['valuationRatios']['child']['dividendYield'] = {'data': dividentYield, 'label': 'Dividend Yield', 'child' : {}, 'value_in': '%', 'description': valuationRatioInst.valuationRatioDividendYield}
    if earningYield and earningYield != {}:
        del earningYield[list(earningYield)[0]]
        stock_detail['valuationRatios']['child']['earningYield'] = {'data': earningYield, 'value_in': '%', 'child' : {},
                                                                   'description': valuationRatioInst.valuationRatioEarningYield if valuationRatioInst else None}
    if bookValues and bookValues != {}:
        stock_detail['valuationRatios']['data']['Price/bookValues'] = bookValues
    # stock_detail['valuationRatios']['data']['Price/Earning'] = {'label': 'Price/Earning','data': {}, 'child':{}}
    # stock_detail['valuationRatios']['data']['EV/EBITDA'] = {'label': 'EV/EBITDA','data': {}, 'child':{}}
    # stock_detail['valuationRatios']['data']['MarketCapital/Sales'] = {'label': 'Market Capital/Sales','data': {}, 'child':{}}
    if stock_detail['valuationRatios']['data'] == {} and stock_detail['valuationRatios']['child'] == {}:
        stock_detail.pop('valuationRatios')

    stock_detail['regulatoryRatios'] = {'label': 'Regulatory Ratios', 'data': {}, 'child': {}}
    if regulatoryRatiosInst_detail and regulatoryRatiosInst_detail != "":
        stock_detail['regulatoryRatios']['data']['CAR'] = RBIGraphDict['CAR']
        stock_detail['regulatoryRatios']['data']['Tier 1'] = RBIGraphDict['tier1']
        stock_detail['regulatoryRatios']['data']['Tier 2'] = RBIGraphDict['tier2']
    if stock_detail['regulatoryRatios']['data'] == {} and stock_detail['regulatoryRatios']['child'] == {}:
        stock_detail.pop('regulatoryRatios')

    stock_detail['NBFCRatios'] = {'label': 'NBFC Ratios', 'data': {}, 'child': {}}
    if tier1CapitalRatioDict and tier1CapitalRatioDict != {}:
        # bankNBFCRatioDescriptionInst.tangibleBookValue
        stock_detail['NBFCRatios']['data']['tier1CapitalRatio'] = {'data': tier1CapitalRatioDict,
                                                                   'description': bankNBFCRatioDescriptionInst.tier1CapitalRatio if bankNBFCRatioDescriptionInst else None}
    if tier2CapitalRatioDict and tier2CapitalRatioDict != {}:
        stock_detail['NBFCRatios']['data']['tier2CapitalRatio'] = {'data': tier2CapitalRatioDict,
                                                                   'description': bankNBFCRatioDescriptionInst.tier2CapitalRatio if bankNBFCRatioDescriptionInst else None}
    if tangibleBookVaueDict and tangibleBookVaueDict != {}:
        stock_detail['NBFCRatios']['data']['tangibleBookVaue'] = {'data': tangibleBookVaueDict,
                                                                  'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                                  'description': bankNBFCRatioDescriptionInst.tangibleBookValue if bankNBFCRatioDescriptionInst else None}
    if aumDict and aumDict != {}:
        stock_detail['NBFCRatios']['data']['aum'] = {'data': aumDict,
                                                     'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                                     'description': bankNBFCRatioDescriptionInst.aum if bankNBFCRatioDescriptionInst else None}
    if aumGrowthDict and aumGrowthDict != {}:
        stock_detail['NBFCRatios']['data']['aumGrowth'] = {'data': aumGrowthDict, 'value_in': '%',
                                                           'description': bankNBFCRatioDescriptionInst.aumGrowth if bankNBFCRatioDescriptionInst else None}

    if stock_detail['NBFCRatios']['data'] == {} and stock_detail['NBFCRatios']['child'] == {}:
        stock_detail.pop('NBFCRatios')

    response_dict.update({'stock': stock_detail})
    """ response_dict.update({
            'stock':stock_detail,
            'stockProfitLoss':stockProfitLoss_list,
            'stockBalanceSheet':stockBalanceSheet_list,
            'cashFlow':stockCashFlow_list,
            'stockGrowthInst' : stockGrowthInst_detail,
            #'createStockGrowth' : createStockGrowth,
            'stockSolvencyInst' : stockSolvencyInst_detail,
            #'createStockSolvency' : createStockSolvency,
            'stockOperatingEfficiencyInst' : stockOperatingEfficiencyInst_detail,
            #'createStockOperatingEfficiency' : createStockOperatingEfficiency,
            'sectorSpecificRatiosInst' : sectorSpecificRatiosInst_detail,
            #'createSectorSpecificRatios' : createSectorSpecificRatios,
            'stockRatiosInst' : stockRatiosInst_detail,
            #'createStockRatios' : createStockRatios,
            'deRatio':processedDeRatio,
            'currentRatio':processedCurrentRatio,
            'quickRatio':processedQuickRatio,
            'interestCoverageRatio':interestCoverageRatio,
            'operatingProfitEBITmargin':operatingProfitEBITmargin,
            'pbtMargin':pbtMargin,
            'patMargin':patMargin,
            'returnOnEquity':returnOnEquity,
            'roce':roce,
            'returnOnAssets':returnOnAssets,
            'returnedGrowthDataRevenue':returnedGrowthDataRevenue,
            'returnedNetProfitGrowthData': returnedNetProfitGrowthData,
            'returnedEPSGrowthData': returnedEPSGrowthData,
            'returnedEBITDAGrowthData': returnedEBITDAGrowthData,
            'returnedPBITGrowthData': returnedPBITGrowthData,
            'processedRevenueGrowthTextual': processedRevenueGrowthTextual,
            'processedNetProfitGrowthTextual': processedNetProfitGrowthTextual,
            'processedEPSGrowthTextual': processedEPSGrowthTextual,
            'processedEBITDAGrowthTextual': processedEBITDAGrowthTextual,
            'processedPBITGrowthTextual': processedPBITGrowthTextual,
            'processedBookValueGrowthTextual':processedBookValueGrowthTextual,
            'processedAssetGrowthTextual':processedAssetGrowthTextual,
            'processedCashFlowGrowthTextual':processedCashFlowGrowthTextual,
            'processedCashFlowGrowthFinancingTextual':processedCashFlowGrowthFinancingTextual,
            #'industrySpecificGraph':industrySpecificGraph,
            #'industrySpecificValsGraph':industrySpecificValsGraph,
            'indusGraphDict':indusGraphDict,
            #'createBookValue':createBookValue,
            'bookValues':bookValues,
            'stockAdmInst':stockAdmInst_detail,
            'despositoryOptions':stockTransferDepositoryOptions_list,
            'saleType':saleTypeOptions_list,
            'bookValuestoEdit':bookValuestoEdit_list,
            'dividentYield':dividentYield,
            'earningYield':earningYield,
            'tier1CapitalRatio': tier1CapitalRatioDict,
            'tier2CapitalRatio': tier2CapitalRatioDict,
            'tangibleBookVaue': tangibleBookVaueDict,
            'aum': aumDict,
            'aumGrowth': aumGrowthDict,
            'valuationRatioInst':valuationRatioInst_details,
            #'valuationRatioInstForm':valuationRatioInstForm,
            'iDescriptionForKeyRatiosInst': iDescriptionForKeyRatiosInst_details,
            'bankNBFCRatioDescriptionInst' : bankNBFCRatioDescriptionInst_detail,
            #'bankNBFCRatioDescriptionInstForm' : bankNBFCRatioDescriptionInstForm,
            'RBIGraphDict': RBIGraphDict,
            'companyForRBIVals': companyForRBIVals_list,
            #'companyRatioCreateForm': companyRatioCreateForm,
            'regulatoryRatiosInst':regulatoryRatiosInst_detail,
            #'regulatoryRatiosInstForm':regulatoryRatiosInstForm,
            'RBICompChart1': RBICompChart1,
            'RBICompChart2': RBICompChart2,
            'RBICompChart3': RBICompChart3,
            'RBICompChart4': RBICompChart4,
    }) """
    return Response({'response': response_dict})


@api_view(['GET'])
def peersViewapi_01(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = {}
        if stock:
            stock_detail = StockSerializer(stock)
            stock_detail = stock_detail.data
        if stock.status == 'draft' and not request.user.is_staff:
            return redirect('websiteApp:buypreIPOUrl')

        renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
        if renderBankNBFCsTemplates:
            return redirect('stockApp:peersViewNBFCapi', slug)
        netProfitMarginCY = revenueCY = 0.00
        allStockList_list = []
        allStockList = stockBasicDetail.objects.all()
        if allStockList:
            for each in allStockList:
                allStockList_ser = StockSerializer(each)
                allStockList_list.append(allStockList_ser.data)
        yearCY = onlyRevenue = ebitda = None
        revenuePeersCompanyList_list = []
        revenuePeersCompanyList = peersCompanyLinking.objects.filter(stockProfileName=stock)
        if revenuePeersCompanyList:
            for each in revenuePeersCompanyList:
                revenuePeersCompanyList_ser = peersCompanyLinkingSerializer(each)
                revenuePeersCompanyList_list.append(revenuePeersCompanyList_ser.data)
        totalInvPY = totalInvCY = totalRevCY = totalIntangiblesCY = totalIntangiblesPY = totalAssetCY = totalAssetPY = netIncomeCY = totalEquityCY = totalEquityPY = EBITCY = longTermDebtCY = longTermDebtPY = 0.00
        totalAssetTurnoverRatioCY = totalFixedAssetTurnoverRatioCY = ROECY = ROCECY = debtToEquity = 0.00
        totalLngDebtCY = currPortLngTermDebtCY = currPortionLeasesCY = lngTermPortionOfLeasesCY = 0.0
        totalLngDebtPY = currPortLngTermDebtPY = currPortionLeasesPY = lngTermPortionOfLeasesPY = 0.0
        totalNonCurrentLiabilityCY = totalNonCurrentLiabilityPY = 0.0

        # revenueGraphData = {}
        screenerDict = {}
        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
        except:
            stockAdmInst = None
        try:
            latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
        except:
            latestProfitAndLoss = 0.00
        try:
            latestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
        except:
            latestBalanceSheet = 0.00
        try:
            secondLatestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('-year')[1:2]
        except:
            secondLatestBalanceSheet = 0.00
        cashAndShortTermBalSheet = minorityInterestVal = totalCalculatedLnDebtCY = 0
        if latestBalanceSheet:
            cashAndShortTermBalSheet = latestBalanceSheet.cashAndShortTermInvestments
            minorityInterestVal = latestBalanceSheet.minorityInterest
            for item in secondLatestBalanceSheet:
                if item:
                    if latestProfitAndLoss != 0.00:
                        if latestProfitAndLoss.revenue:
                            yearCY = latestProfitAndLoss.year
                            if latestProfitAndLoss.revenue:
                                totalRevCY = Decimal(latestProfitAndLoss.revenue)
                            if latestBalanceSheet.totalInventory:
                                totalInvCY = Decimal(latestBalanceSheet.totalInventory)
                            if item.totalInventory:
                                totalInvPY = Decimal(item.totalInventory)
                            if latestBalanceSheet.otherIntangibleAssests:
                                totalIntangiblesCY = Decimal(latestBalanceSheet.otherIntangibleAssests)
                            if item.otherIntangibleAssests:
                                totalIntangiblesPY = Decimal(item.otherIntangibleAssests)
                            if latestBalanceSheet.totalAssets:
                                totalAssetCY = Decimal(latestBalanceSheet.totalAssets)
                            if item.totalAssets:
                                totalAssetPY = Decimal(item.totalAssets)
                            if latestProfitAndLoss.netIncome:
                                netIncomeCY = Decimal(latestProfitAndLoss.netIncome)
                            if latestBalanceSheet.totalEquity:
                                totalEquityCY = Decimal(latestBalanceSheet.totalEquity)
                            if item.totalEquity:
                                totalEquityPY = Decimal(item.totalEquity)
                            if latestProfitAndLoss.pbit:
                                EBITCY = Decimal(latestProfitAndLoss.pbit)
                            if latestBalanceSheet.totalLongTermDebt:
                                totalLngDebtCY = Decimal(latestBalanceSheet.totalLongTermDebt)
                            if item.totalLongTermDebt:
                                totalLngDebtPY = Decimal(item.totalLongTermDebt)
                            if latestBalanceSheet.currentPortionOfLongTermDebt:
                                currPortLngTermDebtCY = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
                            if item.currentPortionOfLongTermDebt:
                                currPortLngTermDebtPY = Decimal(item.currentPortionOfLongTermDebt)
                            if latestBalanceSheet.currentPortionOfLeases:
                                currPortionLeasesCY = Decimal(latestBalanceSheet.currentPortionOfLeases)
                            if item.currentPortionOfLeases:
                                currPortionLeasesPY = Decimal(item.currentPortionOfLeases)
                            if latestBalanceSheet.longTermPortionOfLeases:
                                lngTermPortionOfLeasesCY = Decimal(latestBalanceSheet.longTermPortionOfLeases)
                            if item.longTermPortionOfLeases:
                                lngTermPortionOfLeasesPY = Decimal(item.longTermPortionOfLeases)
                            if latestBalanceSheet.nonCurrentLiabilities:
                                totalNonCurrentLiabilityCY = Decimal(latestBalanceSheet.nonCurrentLiabilities)
                            if item.nonCurrentLiabilities:
                                totalNonCurrentLiabilityPY = Decimal(item.nonCurrentLiabilities)

                            totalCalculatedLnDebtCY = Decimal(totalLngDebtCY) + Decimal(
                                currPortLngTermDebtCY) + Decimal(
                                currPortionLeasesCY) + Decimal(lngTermPortionOfLeasesCY)
                            totalCalculatedLnDebtPY = Decimal(totalLngDebtPY) + Decimal(
                                currPortLngTermDebtPY) + Decimal(
                                currPortionLeasesPY) + Decimal(lngTermPortionOfLeasesPY)

                            totalAssetTurnoverRatioCY = round(
                                totalAssetTurnoverRatioFormula(totalRevCY, totalAssetCY, totalAssetPY), 2)
                            totalFixedAssetTurnoverRatioCY = round(
                                totalFixedAssetTurnoverRatioFormula(totalRevCY, totalInvCY, totalInvPY), 2)
                            ROECY = round(ROEFormula(netIncomeCY, totalEquityCY, totalEquityPY), 2)
                            ROCECY = round(ROCEFormula(EBITCY, totalEquityCY, totalEquityPY, totalNonCurrentLiabilityCY,
                                                       totalNonCurrentLiabilityPY), 2)
                            debtToEquity = round(
                                debtToEquityFormula(totalCalculatedLnDebtCY, totalCalculatedLnDebtPY, totalEquityCY,
                                                    totalEquityPY), 2)
        if latestProfitAndLoss:
            if latestProfitAndLoss.totalRevenue:
                revenueCY = round(latestProfitAndLoss.totalRevenue, 2)
            if latestProfitAndLoss.revenue:
                onlyRevenue = round(latestProfitAndLoss.revenue, 2)
            if latestProfitAndLoss.ebidta:
                ebitda = round(latestProfitAndLoss.ebidta, 2)
            # changes in NPM - Peers starts (Formula changed - It should be revenue of operations insted of Total Revenue )
            netProfitMarginCY = round(
                netProfitMarginFormula(latestProfitAndLoss.netIncome, latestProfitAndLoss.revenue), 2)
        # changes in NPM - Peers ends

        peRatioCS, pbRatioCS = currentStockPEPBView(stock)
        try:
            essentialInst = stockEssentials.objects.get(stockProfileName=stock)
        except:
            essentialInst = None
        marketCapCS = marketCapView(stock)
        if onlyRevenue == 0 or onlyRevenue == None:
            onlyRevenue = 1

        marketCapBySales = return_val_or_0(marketCapCS) / return_val_or_1(onlyRevenue)

        if essentialInst:
            enterpriseValueInst = essentialInst.enterpriseValue
            balanceWithRBIVal = essentialInst.balance_with_RBI
            preferenceEquityVal = essentialInst.preference_equity
        else:
            enterpriseValueInst = 0
            balanceWithRBIVal = preferenceEquityVal = 0
        if ebitda == 0:
            ebitda = 1

        try:
            if stock.stockProfileNameFFU.financialNumbers == 'L':
                marketCapCS = numberConversion(marketCapCS, currentSystem='Cr',
                                               convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        enterpriseVal = return_val_or_0(marketCapCS) - (
                return_val_or_0(cashAndShortTermBalSheet) - return_val_or_0(balanceWithRBIVal)) + return_val_or_0(
            totalCalculatedLnDebtCY) + return_val_or_0(preferenceEquityVal) + return_val_or_0(minorityInterestVal)

        # numberConversion
        # enterpriseVal = numberConversion(enterpriseVal, currentSystem='L', convertTo=stock.stockProfileNameFFU.financialNumbers)
        evByEbitda = round(return_val_or_0(enterpriseVal) / return_val_or_1(ebitda), 2)
        # conversion

        try:
            if stock.stockProfileNameFFU.financialNumbers == 'L':
                marketCapBySales = numberConversion(marketCapBySales, currentSystem='Cr',
                                                    convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        marketCapBySales = round(marketCapBySales, 2)

        stockname = str(stock_detail.get("stockName"))
        screenerDict = {stockname:
            {
                'id': stock.id,
                'type': 'current',
                'revenue': revenueCY,
                'netProfitMargin': netProfitMarginCY,
                'assetTurnoverRation': totalAssetTurnoverRatioCY,
                'totalFixedAssetTurnoverRatio': totalFixedAssetTurnoverRatioCY,
                'ROE': ROECY,
                'ROCE': ROCECY,
                'deptToEquity': debtToEquity,
                'peGraph': peRatioCS,
                'pbGraph': pbRatioCS,
                'marketCap': round(return_val_or_0(marketCapCS), 2),
                'marketCapBySales': marketCapBySales,
                'evByEbitda': evByEbitda,
            }
        }

        fetchForYear = int(currentYear) - 1
        if latestProfitAndLoss:
            if latestProfitAndLoss.year:
                fetchForYear = latestProfitAndLoss.year
        for company in revenuePeersCompanyList:
            if company.stockStatus == 'Listed' and company.screenerLink:
                screenerDict[company.stockName] = crawlScreenerView(company, fetchForYear=fetchForYear)
            else:
                yearlyData = peerLinkingYearlyData.objects.filter(screenerCompany=company)
                yearlyData_list = []
                if yearlyData:
                    for each in yearlyData:
                        yearlyData_serial = peerLinkingYearlyDataSerializer(each)
                        yearlyData_list.append(yearlyData_serial.data)
                try:
                    stockYearData = yearlyData.get(year=fetchForYear)
                    screenerDict[company.stockName] = {
                        'id': company.pk,
                        'type': company.stockStatus,
                        'fetchedUrl': '',
                        'revenue': stockYearData.revenue,
                        'netProfitMargin': stockYearData.netProfitMargin,
                        'assetTurnoverRation': stockYearData.assetTurnoverRation,
                        'ROE': stockYearData.ROE,
                        'ROCE': stockYearData.ROCE,
                        'deptToEquity': stockYearData.deptToEquity,
                        'peGraph': stockYearData.peRatio,
                        'pbGraph': stockYearData.pbRatio,
                        'marketCap': stockYearData.marketCap,
                        'marketCapBySales': stockYearData.marketCapBySales,
                        'enterpriseVal': stockYearData.enterpriseValue,
                        'evByEbitda': stockYearData.evByEbitda,
                        'cashAndShortTermEquivalents': stockYearData.cashAndShortTermCashEquivalents,
                        'PreferenceEquity': stockYearData.PreferenceEquity,
                        'totalMinorityInterest': stockYearData.totalMinorityInterest,
                        'longTermMarketableSecurities': stockYearData.longTermMarketableSecurities,
                        'yearNotAvailable': '',
                        'yearlyData': yearlyData_list,
                    }
                except:
                    screenerDict[company] = {
                        'id': company.pk,
                        'type': company.stockStatus,
                        'fetchedUrl': '',
                        'revenue': 0,
                        'netProfitMargin': 0,
                        'assetTurnoverRation': 0,
                        'ROE': 0,
                        'ROCE': 0,
                        'deptToEquity': 0,
                        'peGraph': 0,
                        'pbGraph': 0,
                        'marketCap': 0,
                        'marketCapBySales': 0,
                        'enterpriseVal': 0,
                        'evByEbitda': 0,
                        'cashAndShortTermEquivalents': 0,
                        'PreferenceEquity': 0,
                        'totalMinorityInterest': 0,
                        'longTermMarketableSecurities': 0,
                        'yearNotAvailable': '',
                        'yearlyData': yearlyData,
                    }
        stockPeersDescInst_detail = ""
        try:
            stockPeersDescInst = stockPeers.objects.get(stockProfileName=stock)
            if stockPeersDescInst:
                stockPeersDescInst_detail = stockPeersSerializer(stockPeersDescInst)
                stockPeersDescInst_detail = stockPeersDescInst_detail.data
        except:
            stockPeersDescInst = None
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        if revenueCY == 0.00 and netProfitMarginCY == 0.00 and \
                totalAssetTurnoverRatioCY == 0.00 and totalFixedAssetTurnoverRatioCY == 0.00 and \
                ROECY == 0.00 and ROCECY == 0.00 and debtToEquity == 0.00 and peRatioCS and \
                pbRatioCS == 0.00 and marketCapCS == 0.00 and marketCapBySales == 0.00 and evByEbitda == 0.00:
            visiblity = False
        else:
            visiblity = True

        response_dict = {}
        stock_detail = {}
        stock_detail['data'] = stockPeersDescInst_detail
        stock_detail['_'] = {'label': '_', 'data': {}, 'child': {}}
        marketCap_dict = {}
        revenue_dict = {}
        netProfit_dict = {}  # currently not found
        netProfitMargin_dict = {}
        netInterestIncome_dict = {}  # currently not found
        priceByBookValue_dict = {}  # currently not found
        priceByEarning_dict = {}  # currently not found
        totalAssetUnderManagement = {}  # currently not found
        roa_dict = {}  # currently not found
        roe_dict = {}
        debtToEquity_dict = {}
        assetTurnoverRation_dict = {}
        evByEbitda_dict = {}
        marketCapBySales_dict = {}

        if screenerDict:
            for company in screenerDict:
                # if type(company) != str:
                #	company = company.stockName

                marketCap_dict[company] = screenerDict[company]['marketCap']
                revenue_dict[company] = screenerDict[company]['revenue']
                netProfitMargin_dict[company] = screenerDict[company]['netProfitMargin']
                roe_dict[company] = screenerDict[company]['ROE']
                debtToEquity_dict[company] = screenerDict[company]['deptToEquity']
                assetTurnoverRation_dict[company] = screenerDict[company]['assetTurnoverRation']
                evByEbitda_dict[company] = screenerDict[company]['evByEbitda']
                marketCapBySales_dict[company] = screenerDict[company]['marketCapBySales']

        if marketCap_dict != {}:
            stock_detail['_']['data']['marketCap'] = marketCap_dict
        if revenue_dict != {}:
            stock_detail['_']['data']['revenue'] = revenue_dict
        if netProfitMargin_dict != {}:
            stock_detail['_']['data']['netProfitMargin'] = netProfitMargin_dict
        if roe_dict != {}:
            stock_detail['_']['data']['roe'] = roe_dict
        if debtToEquity_dict != {}:
            stock_detail['_']['data']['debtToEquity'] = debtToEquity_dict
        if assetTurnoverRation_dict != {}:
            stock_detail['_']['data']['assetTurnoverRatio'] = assetTurnoverRation_dict
        if evByEbitda_dict != {}:
            stock_detail['_']['data']['evByEbitda'] = evByEbitda_dict
        if marketCapBySales_dict != {}:
            stock_detail['_']['data']['marketCapBySales'] = marketCapBySales_dict

        if stock_detail['_']['data'] == {} and stock_detail['_']['child'] == {}:
            stock_detail.pop('_')

        # stock_detail = {'message': company}
        response_dict.update({'stock': stock_detail})
        """context = {
			'stock': stock_detail,
			'allStockList': allStockList_list,
			'stockPeersDescInst': stockPeersDescInst_detail,
			'stockAdmInst': stockAdmInst_detail,
			'despositoryOptions': despositoryOptions,
			'saleType': saleType,
			'visible': visiblity,
			'screenerDict': screenerDict,
			'year': yearCY,
		}
		return Response({'response': context})"""
        return Response({'response': response_dict})


@api_view(['GET'])
def getPeersForBankNBFCView_01(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock).data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    yearCY = totalRevenueCY = netInterestIncomeCY = None
    revenuePeersCompanyList_list = []
    revenuePeersCompanyList = peersCompanyLinkingForBankNBFC.objects.filter(stockProfileName=stock)
    if revenuePeersCompanyList:
        for each in revenuePeersCompanyList:
            revenuePeersCompanyList_list.append(peersCompanyLinkingForBankNBFCSerializer(each).data)
    currentPrice = localOrScreenerPriceView(stock)
    screenerDict = {}
    graphVisiblity = {}
    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst).data
    except:
        stockAdmInst = None
    try:
        latestProfitAndLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestProfitAndLoss = None
    try:
        latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestBalanceSheet = 0.00
    try:
        secondLatestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')[
                                   1:2]
    except:
        secondLatestBalanceSheet = 0.00
    # latest Profit and Loss
    netInterestIncomeCY = totalRevenueCY = netProfitCY = netInterestIncomeCY = dilutedEPSCY = basicEPSCY = 0
    if latestProfitAndLoss:
        yearCY = latestProfitAndLoss.year
        if latestProfitAndLoss.netInterestIncome:
            netInterestIncomeCY = Decimal(latestProfitAndLoss.netInterestIncome)
            graphVisiblity['netInterestIncomeGraph'] = True
        else:
            graphVisiblity['netInterestIncomeGraph'] = False
        if latestProfitAndLoss.totalRevenue:
            totalRevenueCY = Decimal(latestProfitAndLoss.totalRevenue)
            graphVisiblity['revenueGraph'] = True
        else:
            graphVisiblity['revenueGraph'] = False
        if latestProfitAndLoss.netIncome:
            netProfitCY = Decimal(latestProfitAndLoss.netIncome)
        if latestProfitAndLoss.basicEPS:
            basicEPSCY = Decimal(latestProfitAndLoss.basicEPS)
        if latestProfitAndLoss.dilutedEPS:
            dilutedEPSCY = Decimal(latestProfitAndLoss.dilutedEPS)
    # latest Balance Sheet
    totalAssetCY = totalEquityCY = longTermBorrowingsCY = shortTermBorrowingsCY = 0
    leaseLiabilityCY = currentPortionOfLongTermDebtCY = tangibleBookValueCY = 0
    totalCommonSharesOutstandingCY = tier1CapitalRatioCY = tier2CapitalRatioCY = aumCY = 0
    if latestBalanceSheet:
        if latestBalanceSheet.totalAssets:
            totalAssetCY = latestBalanceSheet.totalAssets
        if latestBalanceSheet.totalEquity:
            totalEquityCY = latestBalanceSheet.totalEquity
        if latestBalanceSheet.longTermBorrowings:
            longTermBorrowingsCY = latestBalanceSheet.longTermBorrowings
        if latestBalanceSheet.shortTermBorrowings:
            shortTermBorrowingsCY = latestBalanceSheet.shortTermBorrowings
        if latestBalanceSheet.leaseLiability:
            leaseLiabilityCY = latestBalanceSheet.leaseLiability
        if latestBalanceSheet.currentPortionOfLongTermDebt:
            currentPortionOfLongTermDebtCY = latestBalanceSheet.currentPortionOfLongTermDebt
        if latestBalanceSheet.tangibleBookValue:
            tangibleBookValueCY = latestBalanceSheet.tangibleBookValue
        if latestBalanceSheet.totalCommonSharesOutstanding:
            totalCommonSharesOutstandingCY = latestBalanceSheet.totalCommonSharesOutstanding
        if latestBalanceSheet.tier1CapitalRatio:
            tier1CapitalRatioCY = latestBalanceSheet.tier1CapitalRatio
            graphVisiblity['tier1Graph'] = True
        else:
            graphVisiblity['tier1Graph'] = False
        if latestBalanceSheet.tier2CapitalRatio:
            tier2CapitalRatioCY = latestBalanceSheet.tier2CapitalRatio
            graphVisiblity['tier2Graph'] = True
        else:
            graphVisiblity['tier2Graph'] = False
        if latestBalanceSheet.aum:
            aumCY = latestBalanceSheet.aum
            graphVisiblity['totalAMUGraph'] = True
        else:
            graphVisiblity['totalAMUGraph'] = False
    # Second latest Balance Sheet
    totalAssetsPY = totalEquityPY = longTermBorrowingsPY = shortTermBorrowingsPY = leaseLiabilityPY = currentPortionOfLongTermDebtPY = 0
    for item in secondLatestBalanceSheet:
        if item:
            if item.totalAssets:
                totalAssetsPY = item.totalAssets
            if item.totalEquity:
                totalEquityPY = item.totalEquity
            if item.longTermBorrowings:
                longTermBorrowingsPY = item.longTermBorrowings
            if item.shortTermBorrowings:
                shortTermBorrowingsPY = item.shortTermBorrowings
            if item.leaseLiability:
                leaseLiabilityPY = item.leaseLiability
            if item.currentPortionOfLongTermDebt:
                currentPortionOfLongTermDebtPY = item.currentPortionOfLongTermDebt
    # Calculating Averages
    avgTotalAsset = avgTotalEquity = avgOfSumNumeratorDE = None
    # if totalAssetCY and totalAssetsPY:
    avgTotalAsset = (return_val_or_0(totalAssetCY) + return_val_or_0(totalAssetsPY)) / 2
    # if totalEquityCY and totalEquityPY:
    avgTotalEquity = (return_val_or_0(totalEquityCY) + return_val_or_0(totalEquityPY)) / 2
    sumForDENumeratorCY = sumForDENumeratorPY = None
    # if longTermBorrowingsCY and shortTermBorrowingsCY and leaseLiabilityCY and currentPortionOfLongTermDebtCY:
    sumForDENumeratorCY = return_val_or_0(longTermBorrowingsCY) + return_val_or_0(
        shortTermBorrowingsCY) + return_val_or_0(leaseLiabilityCY) + return_val_or_0(currentPortionOfLongTermDebtCY)
    # if longTermBorrowingsPY and shortTermBorrowingsPY and leaseLiabilityPY and currentPortionOfLongTermDebtPY:
    sumForDENumeratorPY = return_val_or_0(longTermBorrowingsPY) + return_val_or_0(
        shortTermBorrowingsPY) + return_val_or_0(leaseLiabilityPY) + return_val_or_0(currentPortionOfLongTermDebtPY)
    # if sumForDENumeratorCY and sumForDENumeratorPY:
    avgOfSumNumeratorDE = (sumForDENumeratorCY + sumForDENumeratorPY) / 2
    # formulas and calculations
    # if netProfitCY and avgTotalAsset:
    roa = return_val_or_0(netProfitCY) / return_val_or_1(avgTotalAsset)
    if roa and roa != 0:
        graphVisiblity['roaGraph'] = True
    else:
        graphVisiblity['roaGraph'] = False
    # else:
    # 	roa = 0
    # if netProfitCY and netInterestIncomeCY:
    netProfitMarginPercentage = (return_val_or_0(netProfitCY) / return_val_or_1(netInterestIncomeCY)) * 100
    if netProfitMarginPercentage and netProfitMarginPercentage != 0:
        graphVisiblity['netProfitMarginPercentageGraph'] = True
    else:
        graphVisiblity['netProfitMarginPercentageGraph'] = False
    # else:
    # 	netProfitMarginPercentage = 0
    # if netInterestIncomeCY and avgTotalAsset:
    assetTurnOverRatio = return_val_or_0(netInterestIncomeCY) / return_val_or_1(avgTotalAsset)
    if assetTurnOverRatio and assetTurnOverRatio != 0:
        graphVisiblity['assetTurnOverRatioGraph'] = True
    else:
        graphVisiblity['assetTurnOverRatioGraph'] = False
    # else:
    # 	assetTurnOverRatio = 0
    # if netProfitCY and avgTotalEquity:
    roeGraph = False
    roe = return_val_or_0(netProfitCY) / return_val_or_1(avgTotalEquity)
    if roe and roe != 0:
        graphVisiblity['roeGraph'] = True
    else:
        graphVisiblity['roeGraph'] = False
    # else:
    # roe = 0
    # eps = check_eps_basic_or_diluted(basicEPSCY, dilutedEPSCY)
    # if currentPrice and eps:
    # 	priceToEarning = currentPrice / eps
    # else:
    # 	priceToEarning = 0
    priceToEarning, priceToBookVal = currentStockPEPBBankNBFCView(stock)
    if priceToEarning and priceToEarning != 0:
        graphVisiblity['priceToEarningGraph'] = True
    else:
        graphVisiblity['priceToEarningGraph'] = False
    if priceToBookVal and priceToBookVal != 0:
        graphVisiblity['priceToBookValGraph'] = True
    else:
        graphVisiblity['priceToBookValGraph'] = False

    # try:
    # 	bookValueObj = bookValueData.objects.get(stockProfileName=stock,year=yearCY)
    # 	bookValueCY = bookValueObj.bookValue
    # except:
    # 	bookValueCY = 0
    # if currentPrice and bookValueCY:
    # 	if bookValueCY == 0:
    # 		bookValueCY = 1
    # 	priceToBookVal = currentPrice / bookValueCY
    # else:
    # 	priceToBookVal = 0
    # if netInterestIncomeCY and avgTotalAsset:
    nim = return_val_or_0(netInterestIncomeCY) / return_val_or_1(avgTotalAsset)
    if nim and nim != 0:
        graphVisiblity['nimGraph'] = True
    else:
        graphVisiblity['nimGraph'] = False
    # else:
    # 	nim = 0
    # if avgTotalEquity and avgOfSumNumeratorDE:
    debtToEquityRatioGraph = False
    debtToEquityRatio = return_val_or_0(avgOfSumNumeratorDE) / return_val_or_1(avgTotalEquity)
    if debtToEquityRatio and debtToEquityRatio != 0:
        graphVisiblity['debtToEquityRatioGraph'] = True
    else:
        graphVisiblity['debtToEquityRatioGraph'] = False
    # else:
    # 	debtToEquityRatio = 0

    # Coming from Key Ratios
    try:
        rorwaGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock,
                                                                    graphFor='Return on Risk Weighted Assets(RORWA)')
        rorwaInstCY = industrySpecificGraphsValues.objects.get(valuesFor=rorwaGraphFromKeyRatio, year=yearCY)
        RORWAVal = rorwaInstCY.value
        graphVisiblity['RORWAGraph'] = True
    except:
        RORWAVal = 0
        graphVisiblity['RORWAGraph'] = False
    try:
        netNPAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='Net NPA')
        netNPAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=netNPAGraphFromKeyRatio, year=yearCY)
        netNPAVal = netNPAInstCY.value
        graphVisiblity['netNPAGraph'] = True
    except:
        netNPAVal = 0
        graphVisiblity['netNPAGraph'] = False
    try:
        CASAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='CASA')
        CASAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=CASAGraphFromKeyRatio, year=yearCY)
        CASAVal = CASAInstCY.value
        graphVisiblity['casaGraph'] = True
    except:
        CASAVal = 0
        graphVisiblity['casaGraph'] = False
    try:
        grossNPAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='Gross NPA')
        grossNPAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=grossNPAGraphFromKeyRatio, year=yearCY)
        grossNPAVal = grossNPAInstCY.value
        graphVisiblity['grossNPAValGraph'] = True
    except:
        grossNPAVal = 0
        graphVisiblity['grossNPAValGraph'] = False
    try:
        CARGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock,
                                                                  graphFor='Capital Adequacy Ratio(CAR)')
        CARInstCY = industrySpecificGraphsValues.objects.get(valuesFor=CARGraphFromKeyRatio, year=yearCY)
        carVal = CARInstCY.value
        graphVisiblity['carGraph'] = True
    except:
        carVal = 0
        graphVisiblity['carGraph'] = False
    # P/TB Calculation
    # if currentPrice and tangibleBookValueCY and totalCommonSharesOutstandingCY:
    # 	if totalCommonSharesOutstandingCY == 0:
    # 		totalCommonSharesOutstandingCY = 1
    pByTB = return_val_or_0(currentPrice) / return_val_or_1(
        (return_val_or_0(tangibleBookValueCY) * 10000000) / return_val_or_1(totalCommonSharesOutstandingCY))
    if pByTB and pByTB != 0:
        graphVisiblity['pByTBGraph'] = True
    else:
        graphVisiblity['pByTBGraph'] = False
    # else:
    # 	pByTB = 0
    marketCapCS = marketCapView(stock)
    try:
        if stock.stockProfileNameFFU.financialNumbers == 'L':
            marketCapCS = numberConversion(marketCapCS, currentSystem='Cr',
                                           convertTo=stock.stockProfileNameFFU.financialNumbers)
    except:
        pass
    # print('---------------------------------------------------------------------Jhalak new TESTSTING STARTSSSSSSSS---------------------------------------------------------------------')
    # print(marketCapCS)
    # print('---------------------------------------------------------------------Jhalak new TESTSTING ENDDDDDDDSSSS---------------------------------------------------------------------')
    stockname = str(stock_detail.get("stockName"))
    screenerDict[stockname] = {
        'id': stock.id,
        'type': 'current',
        'revenue': round(return_val_or_0(totalRevenueCY), 2),
        'netInterestIncome': round(return_val_or_0(netInterestIncomeCY), 2),

        'marketCap': round(return_val_or_0(marketCapCS), 2),

        'roa': round((roa * 100), 2),
        'netProfitMarginPercentage': round(netProfitMarginPercentage, 2),
        'assetTurnOverRatio': round(assetTurnOverRatio, 2),
        'roe': round((roe * 100), 2),
        'car': round(carVal, 2),
        'netNPA': round(netNPAVal, 2),
        'grossNPA': round(grossNPAVal, 2),
        'stockPE': round(priceToEarning, 2),
        'stockPB': round(priceToBookVal, 2),
        'nim': round((nim * 100), 2),
        'CASA': round(CASAVal, 2),
        'debtToEquityRatio': round(debtToEquityRatio, 2),
        'pByTB': round(pByTB, 2),
        'tier1': round(tier1CapitalRatioCY, 2),
        'tier2': round(tier2CapitalRatioCY, 2),
        'totalAMU': round(aumCY, 2),
        'RORWA': round(RORWAVal, 2),
    }
    fetchForYear = int(currentYear) - 1
    if latestProfitAndLoss:
        if latestProfitAndLoss.year:
            fetchForYear = latestProfitAndLoss.year
    for company in revenuePeersCompanyList:
        if company.stockStatus == 'Listed' and company.screenerLink:
            someVal = crawlScreenerForBankNBFCView(company, fetchForYear=fetchForYear)
            yearlyData_list = []
            if someVal['yearlyData']:
                for each in someVal['yearlyData']:
                    yearlyData_list.append(peerLinkingYearlyDataForBankNBFCSerializer(each).data)
            someVal['yearlyData'] = yearlyData_list
            screenerDict[company.stockName] = someVal
        else:
            unlistedYearlyData_list = []
            unlistedYearlyData = peerLinkingYearlyDataForBankNBFC.objects.filter(screenerCompany=company)
            if unlistedYearlyData:
                unlistedYearlyData_list.append(peerLinkingYearlyDataForBankNBFCSerializer(each).data)

            try:
                companyYearlyInst = unlistedYearlyData.get(year=fetchForYear)
                manualCAR = companyYearlyInst.CAR
                manualMarketCap = companyYearlyInst.marketCap
                manualnetNPA = companyYearlyInst.netNPA
                manualgrossNPA = companyYearlyInst.grossNPA
                manualCASA = companyYearlyInst.CASA
                manualtier1CapitalRatio = companyYearlyInst.tier1CapitalRatio
                manualtier2CapitalRatio = companyYearlyInst.tier2CapitalRatio
                manualtotalAMU = companyYearlyInst.totalAMU
                manualRORWA = companyYearlyInst.RORWA
                manualnumberOfShares = companyYearlyInst.numberOfShares
                manualintangibleAssests = companyYearlyInst.intangibleAssests
                manualnetInterestIncome = companyYearlyInst.netInterestIncome
                manualrevenue = companyYearlyInst.revenue
                manualroa = companyYearlyInst.roa
                manualnetProfitMargin = companyYearlyInst.netProfitMargin
                manualassetTurnOverRatio = companyYearlyInst.assetTurnOverRatio
                manualROE = companyYearlyInst.ROE
                manualpeRatio = companyYearlyInst.peRatio
                manualpbRatio = companyYearlyInst.pbRatio
                manualNIM = companyYearlyInst.NIM
                manualDERatio = companyYearlyInst.DERatio
                manualpriceByTangibleBookRatio = companyYearlyInst.priceByTangibleBookRatio
                if company.screenerLink:
                    manualScreenerLink = company.screenerLink
                else:
                    manualScreenerLink = None
            except:
                manualCAR = 0
                manualMarketCap = 0
                manualnetNPA = 0
                manualgrossNPA = 0
                manualCASA = 0
                manualtier1CapitalRatio = 0
                manualtier2CapitalRatio = 0
                manualtotalAMU = 0
                manualRORWA = 0
                manualnumberOfShares = 0
                manualintangibleAssests = 0
                manualnetInterestIncome = 0
                manualrevenue = 0
                manualroa = 0
                manualnetProfitMargin = 0
                manualassetTurnOverRatio = 0
                manualROE = 0
                manualpeRatio = 0
                manualpbRatio = 0
                manualNIM = 0
                manualDERatio = 0
                manualpriceByTangibleBookRatio = 0
                manualScreenerLink = None
            screenerDict[company.stockName] = {
                'id': company.id,
                'type': 'Unlisted',
                'car': manualCAR,
                'marketCap': manualMarketCap,
                'netNPA': manualnetNPA,
                'grossNPA': manualgrossNPA,
                'CASA': manualCASA,
                'tier1': manualtier1CapitalRatio,
                'tier2': manualtier2CapitalRatio,
                'totalAMU': manualtotalAMU,
                'RORWA': manualRORWA,
                'numberOfShares': manualnumberOfShares,
                'intangibleAssests': manualintangibleAssests,
                'netInterestIncome': manualnetInterestIncome,
                'revenue': manualrevenue,
                'roa': manualroa,
                'netProfitMarginPercentage': manualnetProfitMargin,
                'assetTurnOverRatio': manualassetTurnOverRatio,
                'roe': manualROE,
                'stockPE': manualpeRatio,
                'stockPB': manualpbRatio,
                'nim': manualNIM,
                'debtToEquityRatio': manualDERatio,
                'pByTB': manualpriceByTangibleBookRatio,
                'fetchedUrl': manualScreenerLink,
                'yearlyData': unlistedYearlyData_list,
            }

    # if latestProfitAndLoss:
    # 	if latestProfitAndLoss.year:
    # 		fetchForYear = latestProfitAndLoss.year
    # 	else:
    # 		fetchForYear = 2021
    # for company in revenuePeersCompanyList:
    # 	if company.screenerLink:
    # 		dictForScreenerData = crawlScreenerForBankNBFCView(company, fetchForYear= fetchForYear)
    # 		return HttpResponse(str(dictForScreenerData))
    # 		screenerDict[company] = dictForScreenerData
    stockPeersDescInst_detail = ""
    try:
        stockPeersDescInst = stockPeers.objects.get(stockProfileName=stock)
        if stockPeersDescInst:
            stockPeersDescInst_detail = stockPeersSerializer(stockPeersDescInst).data
    except:
        stockPeersDescInst = None
    peersCompanyDesc = stockPeersForm(instance=stockPeersDescInst)
    peersCompanyLinkingCreate = peersCompanyLinkingForBankNBFCForm()
    # despositoryOptions, saleType = rightSideMenuObjs()
    createpeerLinkingYearlyDataForm = peerLinkingYearlyDataForBankNBFCForm()
    stockPeersDescriptionForBankNBFCInst_detail = ""
    try:
        stockPeersDescriptionForBankNBFCInst = stockPeersDescriptionForBankNBFC.objects.get(stockProfileName=stock)
        if stockPeersDescriptionForBankNBFCInst:
            stockPeersDescriptionForBankNBFCInst_detail = stockPeersDescriptionForBankNBFCSerializer(
                stockPeersDescriptionForBankNBFCInst).data
    except:
        stockPeersDescriptionForBankNBFCInst = None
    stockPeersDescriptionForBankNBFCInstForm = stockPeersDescriptionForBankNBFCForm(
        instance=stockPeersDescriptionForBankNBFCInst)

    if totalRevenueCY == 0.00 and netInterestIncomeCY == 0.00 and \
            marketCapCS == 0.00 and netProfitMarginPercentage == 0.00 and \
            assetTurnOverRatio == 0.00 and roa == 0.00 and roe == 0.00 and carVal and \
            netNPAVal == 0.00 and grossNPAVal == 0.00 and priceToEarning == 0.00 and priceToBookVal == 0.00 and \
            nim == 0.00 and CASAVal == 0.00 and debtToEquityRatio == 0.00 and pByTB == 0.00 and \
            tier1CapitalRatioCY == 0.00 and aumCY == 0.00 and RORWAVal == 0.00:
        visiblity = False
    else:
        visiblity = True

    screenerDict_new = {}
    i = 0
    for company in screenerDict:
        i += 1
        if type(company) != stockBasicDetail:
            screenerDict_new[company] = screenerDict[company]

    response_dict = {}
    stock_detail = {}
    stock_detail['descriptions'] = stockPeersDescInst_detail
    stock_detail['_'] = {'data': {}, 'child': {}}
    marketCap_dict = {}
    revenue_dict = {}
    # netProfit_dict = {} # currently not found
    netInterestIncome_dict = {}
    CASA_dict = {}
    grossNPA_dict = {}
    netNPA_dict = {}
    netInterestMarginDict = {}
    netProfitMargin_dict = {}
    # netInterestIncome_dict = {} # currently not found
    # priceByBookValue_dict = {} # currently not found
    priceByEarning_dict = {}  # currently not found
    totalAssetUnderManagement_dict = {}
    roa_dict = {}
    roe_dict = {}
    car_dict = {}
    debtToEquity_dict = {}
    pByTB_dict = {}
    tier1CapitalRatio_dict = {}
    assetTurnoverRatio_dict = {}
    RORWA_dict = {}
    tier2CapitalRatio_dict = {}
    # evByEbitda_dict = {}
    # marketCapBySales_dict = {}
    if screenerDict:
        for company in screenerDict:
            # if type(company) != str:
            #	company = company.stockName

            marketCap_dict[company] = screenerDict[company]['marketCap']
            revenue_dict[company] = screenerDict[company]['revenue']
            netInterestIncome_dict[company] = screenerDict[company]['netInterestIncome']
            totalAssetUnderManagement_dict[company] = screenerDict[company]['totalAMU']
            CASA_dict[company] = screenerDict[company]['CASA']
            grossNPA_dict[company] = screenerDict[company]['grossNPA']
            netNPA_dict[company] = screenerDict[company]['netNPA']
            netInterestMarginDict[company] = screenerDict[company]['nim']
            netProfitMargin_dict[company] = screenerDict[company]['netProfitMarginPercentage']
            roa_dict[company] = screenerDict[company]['roa']
            roe_dict[company] = screenerDict[company]['roe']
            car_dict[company] = screenerDict[company]['car']
            debtToEquity_dict[company] = screenerDict[company]['debtToEquityRatio']
            pByTB_dict[company] = screenerDict[company]['pByTB']
            tier1CapitalRatio_dict[company] = screenerDict[company]['tier1']
            assetTurnoverRatio_dict[company] = screenerDict[company]['assetTurnOverRatio']
            RORWA_dict[company] = screenerDict[company]['RORWA']
            tier2CapitalRatio_dict[company] = screenerDict[company]['tier2']
        # evByEbitda_dict[company] = screenerDict[company]['evByEbitda']
        # marketCapBySales_dict[company] = screenerDict[company]['marketCapBySales']

    if marketCap_dict != {}:
        stock_detail['_']['data']['marketCap'] = marketCap_dict
    if revenue_dict != {}:
        stock_detail['_']['data']['revenue'] = revenue_dict
    if netInterestIncome_dict != {}:
        stock_detail['_']['data']['netInterestIncome'] = netInterestIncome_dict
    if totalAssetUnderManagement_dict != {}:
        stock_detail['_']['data']['totalAssetUnderManagement'] = totalAssetUnderManagement_dict
    if CASA_dict != {}:
        stock_detail['_']['data']['CASA'] = CASA_dict
    if grossNPA_dict != {}:
        stock_detail['_']['data']['grossNPA'] = grossNPA_dict
    if netNPA_dict != {}:
        stock_detail['_']['data']['netNPA'] = netNPA_dict
    if netInterestMarginDict != {}:
        stock_detail['_']['data']['netInterestMargin'] = netInterestMarginDict
    if netProfitMargin_dict != {}:
        stock_detail['_']['data']['netProfitMargin'] = netProfitMargin_dict
    if roa_dict != {}:
        stock_detail['_']['data']['roa'] = roa_dict
    if roe_dict != {}:
        stock_detail['_']['data']['roe'] = roe_dict
    if car_dict != {}:
        stock_detail['_']['data']['car'] = car_dict
    if debtToEquity_dict != {}:
        stock_detail['_']['data']['debtToEquity'] = debtToEquity_dict
    if pByTB_dict != {}:
        stock_detail['_']['data']['pByTB'] = pByTB_dict
    if tier1CapitalRatio_dict != {}:
        stock_detail['_']['data']['tier1CapitalRatio'] = tier1CapitalRatio_dict
    if assetTurnoverRatio_dict != {}:
        stock_detail['_']['data']['assetTurnoverRatio'] = assetTurnoverRatio_dict
    if RORWA_dict != {}:
        stock_detail['_']['data']['RORWA'] = RORWA_dict
    if tier2CapitalRatio_dict != {}:
        stock_detail['_']['data']['tier2CapitalRatio'] = tier2CapitalRatio_dict

    if stock_detail['_']['data'] == {} and stock_detail['_']['child'] == {}:
        stock_detail.pop('_')
    # stock_detail['_']['data']['assetTurnoverRatio'] = assetTurnoverRation_dict
    # stock_detail['_']['data']['evByEbitda'] = evByEbitda_dict
    # stock_detail['_']['data']['marketCapBySales'] = marketCapBySales_dict
    # stock_detail = {'message': company}
    response_dict.update({'stock': stock_detail})

    context = {
        'stock': stock_detail,
        # 'peersCompanyDesc':peersCompanyDesc,
        'stockPeersDescInst': stockPeersDescInst_detail,
        'stockAdmInst': stockAdmInst_detail,
        # 'peersCompanyLinkingCreate':peersCompanyLinkingCreate,
        'screenerDict': screenerDict,
        'year': yearCY,
        # 'createpeerLinkingYearlyDataForm': createpeerLinkingYearlyDataForm,
        'stockPeersDescriptionForBankNBFCInst': stockPeersDescriptionForBankNBFCInst_detail,
        # 'stockPeersDescriptionForBankNBFCInstForm':stockPeersDescriptionForBankNBFCInstForm,
        'graphVisiblity': graphVisiblity,
        'visible': visiblity,
    }
    return Response({'response': context})


# return render(request, 'UI/peersForBankNBFC.html', context)


@api_view(['GET'])
def newsViewapi_01(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    if request.method == 'GET':
        newsListRaw = {}
        websiteMasterInst = websiteMaster.objects.filter(stockProfileName=stock)
        websiteMasterInst_list = []
        if len(websiteMasterInst):
            for each in websiteMasterInst:
                websiteMasterInst_serial = websiteMasterSerializer(each)
                websiteMasterInst_list.append(websiteMasterInst_serial.data)

        pageType = request.GET.get('type')
        newsDatalist = []
        stockNewsInst_list = []
        newsArticles_list = []
        newsBlog_list = []
        newsVideoShorts_list = []
        newsVideos_list = []
        if pageType == 'articles-only':
            stockNewsInst = stockNews.objects.filter(stockProfileName=stock, newsType='Articles-Only').order_by(
                '-newsPublishDate')
            if len(stockNewsInst):
                for each in stockNewsInst:
                    stockNewsInst_serial = stockNewsSerializer(each)
                    stockNewsInst_list.append(stockNewsInst_serial.data)
            newsArticles = blogArticles.objects.filter(relatedResearchReports=stock).order_by('-dateForListing')
            if len(newsArticles):
                for each in newsArticles:
                    newsArticles_serial = blogArticlesSerializer(each)
                    newsArticles_list.append(newsArticles_serial.data)

            newsBlog = blogNews.objects.filter(relatedResearchReports=stock).order_by('-dateOfNews')
            if len(newsBlog):
                for each in newsBlog:
                    newsBlog_serial = blogNewsSerializer(each)
                    newsBlog_list.append(newsBlog_serial.data)
            for item in stockNewsInst:
                newsObj = vars(
                    newsClubbedObjects(item.title, item.newsPublishDate, item.source_self(), item.get_current_image(),
                                       item.get_absolute_url(), stockNewsSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(newsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            # newsDatalist.append(newsObj)
            for item in newsBlog:
                newsBlogObj = vars(
                    newsClubbedObjects(item.title, item.dateOfNews, 'News Blog', item.get_current_image(),
                                       item.get_absolute_url(), blogNewsSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(newsBlogObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsArticles:
                newsArticlesObj = vars(
                    newsClubbedObjects(item.title, item.dateForListing, 'Article Blog', item.articleImage,
                                       item.get_absolute_url(), blogArticlesSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(newsArticlesObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            with connections['cralwer'].cursor() as cursor:
                status = "'published'"
                SEOTitle = "'" + stock.seoTitle + "'"
                query = 'Select title, date, site, img, link from "crawlApp_googlenewsstore" where status=' + status + ' AND "connectedStock"=' + SEOTitle + ';'
                cursor.execute(query)
                newsListRaw = cursor.fetchall()
                for item in newsListRaw:
                    newsLink = 'https://' + str(item[4])
                    if item[3]:
                        imgLink = item[3]
                    else:
                        imgLink = stock.logo.url
                    crawledNewsSelf = vars(newsClubbedObjects(item[0], item[1], item[2], imgLink, newsLink, item))
                    employeeJSONData = EmployeeEncoder().encode(crawledNewsSelf)
                    employeeJSON = json.loads(employeeJSONData)
                    newsDatalist.append(employeeJSON)
        elif pageType == 'videos-only':
            stockNewsInst = stockNews.objects.filter(stockProfileName=stock, newsType='Videos-Only').order_by(
                '-newsPublishDate')
            if len(stockNewsInst):
                for each in stockNewsInst:
                    stockNewsInst_serial = stockNewsSerializer(each)
                    stockNewsInst_list.append(stockNewsInst_serial.data)
            newsVideoShorts = blogVideosShorts.objects.filter(relatedResearchReports=stock).order_by('-releaseDate')
            if len(newsVideoShorts):
                for each in newsVideoShorts:
                    newsVideoShorts_serial = blogVideosShortsSerializer(each)
                    newsVideoShorts_list.append(newsVideoShorts_serial.data)
            newsVideos = blogVideos.objects.filter(relatedResearchReports=stock).order_by('-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideos_list.append(newsVideos_serial.data)
            for item in stockNewsInst:
                newsObj = vars(
                    newsClubbedObjects(item.title, item.newsPublishDate, item.source_self(), item.get_current_image(),
                                       item.get_absolute_url(), stockNewsSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(newsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsVideoShorts:
                if item.releaseDate:
                    itemDate = item.releaseDate.date()
                else:
                    itemDate = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d').date()
                shortsObj = vars(newsClubbedObjects(item.title, itemDate, 'Shorts Blog', item.get_current_image(),
                                                    item.get_absolute_url(), blogVideosShortsSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(shortsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsVideos:
                videosObj = vars(
                    newsClubbedObjects(item.title, item.releasedDate, 'Video Blog', item.get_current_image(),
                                       item.get_absolute_url(), blogVideosSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(videosObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
        else:
            newsBlog = blogNews.objects.filter(relatedResearchReports=stock).order_by('-dateOfNews')
            if len(newsBlog):
                for each in newsBlog:
                    newsBlog_serial = blogNewsSerializer(each)
                    newsBlog_list.append(newsBlog_serial.data)
            newsVideoShorts = blogVideosShorts.objects.filter(relatedResearchReports=stock).order_by('-releaseDate')
            if len(newsVideoShorts):
                for each in newsVideoShorts:
                    newsVideoShorts_serial = blogVideosShortsSerializer(each)
                    newsVideoShorts_list.append(newsVideoShorts_serial.data)
            newsVideos = blogVideos.objects.filter(relatedResearchReports=stock).order_by('-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideos_list.append(newsVideos_serial.data)
            newsArticles = blogArticles.objects.filter(relatedResearchReports=stock).order_by('-dateForListing')
            if len(newsArticles):
                for each in newsArticles:
                    newsArticles_serial = blogArticlesSerializer(each)
                    newsArticles_list.append(newsArticles_serial.data)
            stockNewsInst = stockNews.objects.filter(stockProfileName=stock).order_by('-newsPublishDate')
            if len(stockNewsInst):
                for each in stockNewsInst:
                    stockNewsInst_serial = stockNewsSerializer(each)
                    stockNewsInst_list.append(stockNewsInst_serial.data)
            for item in stockNewsInst:
                # newsObj = vars(newsClubbedObjects(item.get('title'), item.get('newsPublishDate'), item.get('source_self'),
                #                             item.get('get_current_image'), item.get('get_absolute_url'), item))
                newsObj = vars(
                    newsClubbedObjects(item.title, item.newsPublishDate, item.source_self(), item.get_current_image(),
                                       item.get_absolute_url(), stockNewsSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(newsObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            # print(newsVideoShorts)
            for item in newsVideoShorts:
                if item.releaseDate:
                    itemDate = item.releaseDate.date()
                else:
                    itemDate = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d').date()
                shortsObj = vars(newsClubbedObjects(item.title, itemDate, 'Shorts Blog', item.get_current_image(),
                                                    item.get_absolute_url(), blogVideosShortsSerializer(item).data))
                # print(shortsObj)
                employeeJSONData = EmployeeEncoder().encode(shortsObj)
                # print(employeeJSONData)
                employeeJSON = json.loads(employeeJSONData)
                # print(employeeJSON)
                newsDatalist.append(employeeJSON)

            for item in newsBlog:
                newsBlogObj = vars(
                    newsClubbedObjects(item.title, item.dateOfNews, 'News Blog', item.get_current_image(),
                                       item.get_absolute_url(), blogNewsSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(newsBlogObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsVideos:
                videosObj = vars(
                    newsClubbedObjects(item.title, item.releasedDate, 'Video Blog', item.get_current_image(),
                                       item.get_absolute_url(), blogVideosSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(videosObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            for item in newsArticles:
                newsArticlesObj = vars(
                    newsClubbedObjects(item.title, item.dateForListing, 'Article Blog', item.articleImage,
                                       item.get_absolute_url(), blogArticlesSerializer(item).data))
                employeeJSONData = EmployeeEncoder().encode(newsArticlesObj)
                employeeJSON = json.loads(employeeJSONData)
                newsDatalist.append(employeeJSON)
            with connections['cralwer'].cursor() as cursor:
                status = "'published'"
                SEOTitle = "'" + stock.seoTitle + "'"
                query = 'Select title, date, site, img, link from "crawlApp_googlenewsstore" where status=' + status + ' AND "connectedStock"=' + SEOTitle + ' order by date desc;'
                cursor.execute(query)
                newsListRaw = cursor.fetchall()
                for item in newsListRaw:
                    newsLink = 'https://' + str(item[4])
                    crawledNewsSelf = vars(newsClubbedObjects(item[0], item[1], item[2], item[3], newsLink, item))
                    employeeJSONData = EmployeeEncoder().encode(crawledNewsSelf)
                    employeeJSON = json.loads(employeeJSONData)
                    newsDatalist.append(employeeJSON)
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_ser = stockAdminSerializer(stockAdmInst)
                stockAdmInst = stockAdmInst_ser.data
        except:
            stockAdmInst = None
        despositoryOptions, saleType = rightSideMenuObjs_serialized()

        # newsDatalist.sort(key=lambda x: x.releaseDate_self, reverse=True)

        # description field for SEO - starts
        stockNewsSEOInst_dict = {}
        try:
            stockNewsSEOInst = stockNewsSEO.objects.get(stockProfileName=stock)
            if stockNewsSEOInst:
                serializer = stockNewsSEOSerializer(stockNewsSEOInst)
                stockNewsSEOInst_dict.update(serializer.data)

        except:
            stockNewsSEOInst = None
        # description field for SEO - ends

        response_dict = {}
        stock_detail = {}
        stock_detail['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle,
                                     'description': stockNewsSEOInst.newsDescriptionSEO if stockNewsSEOInst else None}
        stock_detail['videos&Articles'] = {'label': 'Videos & Articles', 'data': {}, 'child': {}}
        # if stockNewsInst_list and stockNewsInst_list!=[]:
        if newsDatalist and newsDatalist != []:
            newsDatalist_new = []
            for item in newsDatalist:
                temp = {}
                try:
                    temp['newsType'] = item['completeObject']['newsType']
                except:
                    temp['newsType'] = 'Videos-Only' if item['source_self'] in ['Shorts Blog',
                                                                                'Video Blog'] else 'Articles-Only'
                temp['websiteLink'] = item['get_absolute_url']
                temp['thumbnail'] = item['get_current_image']
                temp['title'] = item['title']
                try:
                    temp['referalWebsiteName'] = item['source_self']
                except:
                    if 'completeObject' in item:
                        temp['referalWebsiteName'] = item['completeObject']['referalWebsiteName']
                    else:
                        temp['referalWebsiteName'] = None

                date = f"{item['releaseDate_self']['year']}-{item['releaseDate_self']['month']}-{item['releaseDate_self']['day']}"
                temp['newsPublishDate'] = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d %B %Y')

                newsDatalist_new.append(temp)

            stock_detail['videos&Articles']['data']['videos&Articles'] = newsDatalist_new

        if stock_detail['videos&Articles']['data'] == {} and stock_detail['videos&Articles']['child'] == {}:
            stock_detail.pop('videos&Articles')

        stock_detail['disclaimer'] = {'label': 'Disclaimer', 'data': {}, 'child': {}}

        investmentDisclaimer_dict = {}
        planifyDisclaimer_dict = {}
        transactionDisclaimer_dict = {}

        if websiteMasterInst_list and websiteMasterInst_list != []:
            for item in websiteMasterInst_list:
                if item['title'] == 'Investment Disclaimer':
                    investmentDisclaimer_dict = item
                elif item['title'] == 'Planify Disclaimer':
                    planifyDisclaimer_dict = item
                elif item['title'] == 'Transaction Disclaimer':
                    transactionDisclaimer_dict = item
        if investmentDisclaimer_dict and investmentDisclaimer_dict != {}:
            stock_detail['disclaimer']['child']['investmentDisclaimer'] = {'data': investmentDisclaimer_dict,
                                                                           'child': {}}
        # stock_detail['disclaimer']['child']['investmentDisclaimer']['data'] = investmentDisclaimer_dict
        if planifyDisclaimer_dict and planifyDisclaimer_dict != {}:
            stock_detail['disclaimer']['child']['planifyDisclaimer'] = {'data': planifyDisclaimer_dict, 'child': {}}
        if transactionDisclaimer_dict and transactionDisclaimer_dict != {}:
            stock_detail['disclaimer']['child']['transactionDisclaimer'] = {'data': transactionDisclaimer_dict,
                                                                            'child': {}}

        if stock_detail['disclaimer']['data'] == {} and stock_detail['disclaimer']['child'] == {}:
            stock_detail.pop('disclaimer')

        response_dict.update({'stock': stock_detail})
        return Response({'response': response_dict})


@api_view(['GET'])
def eventsViewapi_01(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    if request.method == 'GET':
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_ser = stockAdminSerializer(stockAdmInst)
                stockAdmInst = stockAdmInst_ser.data
        except:
            stockAdmInst = None

        stockEventsDividendInst = stockEventsDividend.objects.filter(stockProfileName=stock).order_by(
            '-exDateFrDividend')
        pastDividents = []
        futureDividents = []
        for item in stockEventsDividendInst:
            if str(item.exDateFrDividend) > today:
                futureDividents.append(EmployeeEncoder().encode(item))
            else:
                pastDividents.append(EmployeeEncoder().encode(item))
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        stockEventsCorpActionsInst = stockEventsCorpActions.objects.filter(stockProfileName=stock).order_by(
            '-exDateFrCorporate')
        pastCorpActions = []
        futureCorpActions = []
        for item in stockEventsCorpActionsInst:
            if str(item.exDateFrCorporate) > today:
                futureCorpActions.append(EmployeeEncoder().encode(item))
            else:
                pastCorpActions.append(EmployeeEncoder().encode(item))

        stockEventsAnnouncementsInst = stockEventsAnnouncements.objects.filter(stockProfileName=stock).order_by(
            '-dateFrAnnouncement')
        pastAnnouncements = []
        futureAnnouncements = []
        for item in stockEventsAnnouncementsInst:
            if str(item.dateFrAnnouncement) > today:
                futureAnnouncements.append(EmployeeEncoder().encode(item))
            else:
                pastAnnouncements.append(EmployeeEncoder().encode(item))

        stockEventsLegalOrdersInst_list = []
        stockEventsLegalOrdersInst = stockEventsLegalOrders.objects.filter(stockProfileName=stock).order_by(
            '-exDateFrLegalOrders')
        if stockEventsLegalOrdersInst:
            for each in stockEventsLegalOrdersInst:
                stockEventsLegalOrdersInst_serial = stockEventsLegalOrdersSerializer(each)
                stockEventsLegalOrdersInst_list.append(stockEventsLegalOrdersInst_serial.data)

        # description field for SEO - starts
        try:
            stockEventsSEOInst = stockEventsSEO.objects.get(stockProfileName=stock)
            if stockEventsSEOInst:
                stockEventsSEOInst_ser = stockEventsSEOSerializer(stockEventsSEOInst)
                stockEventsSEOInst = stockEventsSEOInst_ser.data
        except:
            stockEventsSEOInst = None

        # description field for SEO - ends
        response_dict = {}
        stock_detail = {}
        stock_detail['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle}
        stock_detail['dividends'] = {'label': 'Dividends', 'data': {}, 'child': {}}
        # dividendTypeOptions
        pastDividents_list = []
        futureDividents_list = []
        false = False
        true = True
        null = None
        if pastDividents and pastDividents != []:
            for item in pastDividents:
                item = eval(item)
                tmp = {}
                try:
                    tmp['dividentType'] = get_object_or_404(dividendTypeOptions, id=item['dividendType_id']).name
                except:
                    tmp['dividentType'] = item['dividendType_id']
                tmp['dividendShare'] = item['dividendShare']
                tmp['exDateFrDividend'] = item['exDateFrDividend']
                pastDividents_list.append(tmp)

        if futureDividents and futureDividents != []:
            for item in futureDividents:
                item = eval(item)
                tmp = {}
                try:
                    tmp['dividentType'] = get_object_or_404(dividendTypeOptions, id=item['dividendType_id']).name
                except:
                    tmp['dividentType'] = item['dividendType_id']
                tmp['dividendShare'] = item['dividendShare']
                tmp['exDateFrDividend'] = item['exDateFrDividend']
                futureDividents_list.append(tmp)
        if pastDividents_list and pastDividents_list != []:
            stock_detail['dividends']['data']['pastDividends'] = pastDividents_list
        if futureDividents_list and futureDividents_list != []:
            stock_detail['dividends']['data']['futureDividends'] = futureDividents_list

        if stock_detail['dividends']['data'] == {} and stock_detail['dividends']['child'] == {}:
            stock_detail.pop('dividends')

        stock_detail['corporateActions'] = {'label': 'Corporate Actions', 'data': {}, 'child': {}}
        pastCorpActions_list = []
        futureCorpActions_list = []
        if pastCorpActions and pastCorpActions != []:
            for item in pastCorpActions:
                item = eval(item)
                tmp = {}
                try:
                    tmp['corporateActionsName'] = get_object_or_404(corpActionsOptions,
                                                                    id=item['corporateActionsName_id']).name
                except:
                    tmp['corporateActionsName'] = item['corporateActionsName_id']
                tmp['corporateActionsDescription'] = item['corporateActionsDescription']
                tmp['ratio'] = item['ratio']
                tmp['exDateFrCorporate'] = item['exDateFrCorporate']
                pastCorpActions_list.append(tmp)

        if futureCorpActions and futureCorpActions != []:
            for item in futureCorpActions:
                item = eval(item)
                tmp = {}
                try:
                    tmp['corporateActionsName'] = get_object_or_404(corpActionsOptions,
                                                                    id=item['corporateActionsName_id']).name
                except:
                    tmp['corporateActionsName'] = item['corporateActionsName_id']
                tmp['corporateActionsDescription'] = item['corporateActionsDescription']
                tmp['ratio'] = item['ratio']
                tmp['exDateFrCorporate'] = item['exDateFrCorporate']
                futureCorpActions_list.append(tmp)

        if pastCorpActions_list and pastCorpActions_list != []:
            stock_detail['corporateActions']['data']['pastCorpActions'] = pastCorpActions_list
        if futureCorpActions_list and futureCorpActions_list != []:
            stock_detail['corporateActions']['data']['futureCorpActions'] = futureCorpActions_list

        if stock_detail['corporateActions']['data'] == {} and stock_detail['corporateActions']['child'] == {}:
            stock_detail.pop('corporateActions')

        stock_detail['announcements'] = {'label': 'Announcements', 'data': {}, 'child': {}}

        pastAnnouncements_list = []
        futureAnnouncements_list = []
        if pastAnnouncements and pastAnnouncements != []:
            for item in pastAnnouncements:
                item = eval(item)
                tmp = {}
                try:
                    tmp['announcementTitle'] = get_object_or_404(announcementTypeOptions,
                                                                 id=item['announcementTitle_id']).name
                except:
                    tmp['announcementTitle'] = item['announcementTitle_id']
                tmp['announcementBrief'] = item['announcementBrief']
                tmp['linkUrlFrAnnouncement'] = item['linkUrlFrAnnouncement']
                tmp['linkFrAnnouncement'] = item['linkFrAnnouncement']
                tmp['dateFrAnnouncement'] = item['dateFrAnnouncement']
                pastAnnouncements_list.append(tmp)

        if futureAnnouncements and futureAnnouncements != []:
            for item in futureAnnouncements:
                item = eval(item)
                tmp = {}
                try:
                    tmp['announcementTitle'] = get_object_or_404(announcementTypeOptions,
                                                                 id=item['announcementTitle_id']).name
                except:
                    tmp['announcementTitle'] = item['announcementTitle_id']
                tmp['announcementBrief'] = item['announcementBrief']
                tmp['linkUrlFrAnnouncement'] = item['linkUrlFrAnnouncement']
                tmp['linkFrAnnouncement'] = item['linkFrAnnouncement']
                tmp['dateFrAnnouncement'] = item['dateFrAnnouncement']
                futureAnnouncements_list.append(tmp)

        if pastAnnouncements_list and pastAnnouncements_list != []:
            stock_detail['announcements']['data']['pastAnnouncements'] = pastAnnouncements_list
        if futureAnnouncements_list and futureAnnouncements_list != []:
            stock_detail['announcements']['data']['futureAnnouncements'] = futureAnnouncements_list

        if stock_detail['announcements']['data'] == {} and stock_detail['announcements']['child'] == {}:
            stock_detail.pop('announcements')

        stock_detail['legalOrders'] = {'label': 'Legal Orders', 'data': {}, 'child': {}}

        stockEventsLegalOrdersInst_list_new = []
        if stockEventsLegalOrdersInst_list and stockEventsLegalOrdersInst_list != []:
            for item in stockEventsLegalOrdersInst_list:
                tmp = {}
                tmp['caseTitle'] = item['caseTitle']
                tmp['caseNumber'] = item['caseNumber']
                tmp['linkUrlFrLegalOrders'] = item['linkUrlFrLegalOrders']
                tmp['linkFrLegalOrders'] = item['linkFrLegalOrders']
                tmp['exDateFrLegalOrders'] = item['exDateFrLegalOrders']
                stockEventsLegalOrdersInst_list_new.append(tmp)

        if stockEventsLegalOrdersInst_list_new and stockEventsLegalOrdersInst_list_new != []:
            stock_detail['legalOrders']['data']['legalOrders'] = stockEventsLegalOrdersInst_list_new

        if stock_detail['legalOrders']['data'] == {} and stock_detail['legalOrders']['child'] == {}:
            stock_detail.pop('legalOrders')

        response_dict.update({'stock': stock_detail})
        return Response({'response': response_dict})

@api_view(['GET'])
def ownershipViewapi_01(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    if request.method == 'GET':

        try:
            ownershipInst = stockOwnership.objects.get(stockProfileName=stock)
            if ownershipInst:
                ownershipInst_ser = stockOwnershipSerializer(ownershipInst)
                ownershipInst = ownershipInst_ser.data
        except:
            ownershipInst = None

        ownershipDirectorInst_list = []
        ownershipInstitutionalInst_list = []
        ownershipPatternInst_list = []

        ownershipDirectorInst = stockOwnershipDirector.objects.filter(stockProfileName=stock)
        if ownershipDirectorInst:
            for each in ownershipDirectorInst:
                ownershipDirectorInst_ser = stockOwnershipDirectorSerializer(each)
                ownershipDirectorInst_data = ownershipDirectorInst_ser.data
                ownershipDirectorInst_list.append(ownershipDirectorInst_data)

        ownershipInstitutionalInst = stockOwnershipInstitutional.objects.filter(stockProfileName=stock)
        if ownershipInstitutionalInst:
            for each in ownershipInstitutionalInst:
                ownershipInstitutionalInst_ser = stockOwnershipInstitutionalSerializer(each)
                ownershipInstitutionalInst_data = ownershipInstitutionalInst_ser.data
                ownershipInstitutionalInst_list.append(ownershipInstitutionalInst_data)
        ownershipPatternInst = stockOwnershipPattern.objects.filter(stockProfileName=stock).order_by('-year')
        if ownershipPatternInst:
            for each in ownershipPatternInst:
                ownershipPatternInst_ser = stockOwnershipPatternSerializer(each)
                ownershipPatternInst_data = ownershipPatternInst_ser.data
                ownershipPatternInst_list.append(ownershipPatternInst_data)

        totalPromoterholdingValue = mutualFundHoldingValue = domesticInstitutionalHoldingsValue = foreignInstitutionalHoldingsValue = others = institutionalHolding = publicInstitutionalHoldings = nonPublicInstitutionalHoldings = retail = employees = custodians = promoters = privatePublicInvestmenFirmVCs = False

        for item in ownershipPatternInst:
            if item.totalPromoterholdingValue:
                totalPromoterholdingValue = True
            if item.mutualFundHoldingValue:
                mutualFundHoldingValue = True
            if item.domesticInstitutionalHoldingsValue:
                domesticInstitutionalHoldingsValue = True
            if item.foreignInstitutionalHoldingsValue:
                foreignInstitutionalHoldingsValue = True
            if item.others:
                others = True
            if item.institutionalHolding:
                institutionalHolding = True
            if item.publicInstitutionalHoldings:
                publicInstitutionalHoldings = True
            if item.nonPublicInstitutionalHoldings:
                nonPublicInstitutionalHoldings = True
            if item.retail:
                retail = True
            if item.employees:
                employees = True
            if item.custodians:
                custodians = True
            if item.promoters:
                promoters = True
            if item.privatePublicInvestmenFirmVCs:
                privatePublicInvestmenFirmVCs = True

        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_ser = stockAdminSerializer(stockAdmInst)
                stockAdmInst = stockAdmInst_ser.data
        except:
            stockAdmInst = None
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        staticUrl = settings.STATIC_URL

        response_dict = {}
        stock_detail = {}
        stock_detail['extraData'] = {'seoTitle': stock.seoTitle, 'stockName': stock.stockName}
        if ownershipInst:
            stock_detail['ownershipInst'] = ownershipInst

        # stock_detail['ownershipPatternInst'] = ownershipPatternInst_list
        stock_detail['shareholdingPattern'] = {'label': 'Shareholding Pattern', 'data': ownershipPatternInst_list,
                                               'child': {}}

        if stock_detail['shareholdingPattern']['data'] == {} and stock_detail['shareholdingPattern']['child'] == {}:
            stock_detail.pop('shareholdingPattern')

        stock_detail['management'] = {'label': 'Management', 'data': {}, 'child': {}}

        if stock_detail['management']['data'] == {} and stock_detail['management']['child'] == {}:
            stock_detail.pop('management')

        stock_detail['boardOfDirectors'] = {'label': 'Board of Directors', 'data': {}, 'child': {}}
        if ownershipDirectorInst_list and ownershipDirectorInst_list != []:

            ownershipDirectorInst_list_new = []
            for item in ownershipDirectorInst_list:
                tmp = {}
                tmp['directorName'] = item['directorName']
                tmp['gender'] = item['gender']
                tmp['directorTitle'] = item['directorTitle']
                tmp['directorImage'] = item['directorImage']
                tmp['directorImageAlt'] = item['directorImageAlt']
                ownershipDirectorInst_list_new.append(tmp)

            stock_detail['boardOfDirectors']['data']['boardOfDirectors'] = ownershipDirectorInst_list_new

        if stock_detail['boardOfDirectors']['data'] == {} and stock_detail['boardOfDirectors']['child'] == {}:
            stock_detail.pop('boardOfDirectors')

        stock_detail['investors'] = {'label': 'Investors', 'data': {}, 'child': {}}
        if ownershipInstitutionalInst_list and ownershipInstitutionalInst_list != []:

            ownershipInstitutionalInst_list_new = []
            for item in ownershipInstitutionalInst_list:
                tmp = {}
                tmp['institutionName'] = item['institutionName']
                tmp['fundName'] = item['fundName']
                tmp['institutionImage'] = item['institutionImage']
                tmp['institutionImageAlt'] = item['institutionImageAlt']
                tmp['noOfShares'] = item['noOfShares']
                tmp['percentageHolding'] = item['percentageHolding']
                ownershipInstitutionalInst_list_new.append(tmp)

            stock_detail['investors']['data']['investors'] = ownershipInstitutionalInst_list_new

        if stock_detail['investors']['data'] == {} and stock_detail['investors']['child'] == {}:
            stock_detail.pop('investors')

        response_dict.update({'stock': stock_detail})

        return Response({'response': response_dict})


@api_view(['GET'])
def pitchViewAPI_01(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        try:
            highLights_data = highLights.objects.filter(stockProfileName_id=stock.id)
            highLights_serializer = highLightsSerializer(highLights_data, many=True)
            highlights_data = highLights_serializer.data
        except:
            highlights_data = None
        try:
            stockInvestmentChecklist_response = stockInvestmentChecklist.objects.filter(stockProfileName_id=stock.id)
            stockInvestmentChecklist_serializer = stockInvestmentChecklistSerializer(stockInvestmentChecklist_response,
                                                                                     many=True)
            stockInvestmentChecklist_data = stockInvestmentChecklist_serializer.data
        except:
            stockInvestmentChecklist_data = None

        try:
            stockOwnershipDirector_response = stockOwnershipDirector.objects.filter(stockProfileName_id=stock.id)
            stockOwnershipDirector_serializer = stockOwnershipDirectorSerializer(stockOwnershipDirector_response,
                                                                                 many=True)
            stockOwnershipDirector_data = stockOwnershipDirector_serializer.data
        except:
            stockOwnershipDirector_data = None

        try:
            deck_response = deck.objects.filter(stockProfileName_id=stock.id)
            deck_serializer = deckSerializer(deck_response, many=True)
            deck_data = deck_serializer.data
        except:
            deck_data = None

        try:
            deck_response = deck_images.objects.filter(deckname__stockProfileName=stock.id)
            deckimages_serializer = deck_imagesSerializer(deck_response, many=True)
            deckimages_data = deckimages_serializer.data
        except:
            deckimages_data = None

        newsVideoShorts_list = []
        newsVideospitch_list = []
        newsVideoshead_list = []
        try:
            newsVideoShorts = blogVideosShorts.objects.filter(relatedResearchReports=stock).order_by('-releaseDate')
            if len(newsVideoShorts):
                for each in newsVideoShorts:
                    newsVideoShorts_serial = blogVideosShortsSerializer(each)
                    newsVideoShorts_list.append(newsVideoShorts_serial.data)
        except:
            newsVideoShorts_list = []
        try:
            newsVideos = blogVideos.objects.filter(showinpitch=True, relatedResearchReports=stock).order_by(
                '-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideospitch_list.append(newsVideos_serial.data)
        except:
            newsVideospitch_list = []

        try:
            newsVideos = blogVideos.objects.filter(showinhead=True, relatedResearchReports=stock).order_by(
                '-releasedDate')
            if len(newsVideos):
                for each in newsVideos:
                    newsVideos_serial = blogVideosSerializer(each)
                    newsVideoshead_list.append(newsVideos_serial.data)
        except:
            newsVideoshead_list = []

        try:
            stock_serializer = StockSerializer(stock)
            heading = stock_serializer.data["headingForStartup"]
            type_Of_Shares = stock_serializer.data["type_Of_Shares"]
            shareDematerialized = stock_serializer.data["shareDematerialized"]
        except:
            heading = None
            type_Of_Shares = None
            shareDematerialized = None

        type_of_company = None
        try:
            essentialInst = stockEssentials.objects.filter(stockProfileName=slug)
            for each in essentialInst:
                type_of_company = each.typeOfCompany.name
        except:
            type_of_company = None

        context = {
            "highights": highlights_data,
            "newsVideospitch": newsVideospitch_list,
            "newsVideoshead": newsVideoshead_list,
            "stockInvestmentChecklist": stockInvestmentChecklist_data,
            "stockOwnershipDirector": stockOwnershipDirector_data,
            "deck": deck_data,
            "deck_images": deckimages_data,
            "newsVideosshorts": newsVideoShorts_list,
            "heading": heading,
            "type_Of_Shares": type_Of_Shares,
            "shareDematerialized": shareDematerialized,
            "type_of_company": type_of_company

        }
        null = None
        true = True
        false = False
        context1 = {"highights": [
            {
                "id": 4,
                "description": "this is the Pitch for tata-technologies",
                "icon": "https://testing-planify.s3.amazonaws.com/media/stock/images/highLightsicon/sample_mCiQnbe.jpg",
                "stockProfileName": 61
            },
            {
                "id": 5,
                "description": "this is the Pitch for tata-technologies",
                "icon": "https://testing-planify.s3.amazonaws.com/media/stock/images/highLightsicon/sample_z12W9UW.jpg",
                "stockProfileName": 61
            },
            {
                "id": 6,
                "description": "this is the Pitch for tata-technologies second",
                "icon": "https://testing-planify.s3.amazonaws.com/media/stock/images/highLightsicon/sample_tKinuVI.jpg",
                "stockProfileName": 61
            },
            {
                "id": 1,
                "description": "this is the Pitch for tata-technologies second",
                "icon": "https://testing-planify.s3.amazonaws.com/media/stock/images/highLightsicon/images2.jpeg",
                "stockProfileName": 61
            },
            {
                "id": 7,
                "description": "this is the Pitch for tata-technologies second check 2",
                "icon": "https://testing-planify.s3.amazonaws.com/media/stock/images/highLightsicon/images2_Gu5R0cb.jpeg",
                "stockProfileName": 61
            },
            {
                "id": 8,
                "description": "this is the Pitch for tata-technologies first",
                "icon": null,
                "stockProfileName": 61
            },
            {
                "id": 9,
                "description": "this is the Pitch for tata-technologies first iiiiiiiiiii",
                "icon": null,
                "stockProfileName": 61
            },
            {
                "id": 3,
                "description": "this is the Pitch for tata-technologies first iiiiiiiiiii",
                "icon": "https://testing-planify.s3.amazonaws.com/media/stock/images/highLightsicon/sample_k1HwAxL.jpg",
                "stockProfileName": 61
            }
        ],
            "newsVideospitch": [
                {
                    "id": 84,
                    "title": "Tata Technologies Limited Pre IPO Unlisted Shares - Complete Review & Analysis - Planify",
                    "slug": "tata-technologies-limited-pre-ipo-unlisted-shares",
                    "subTitle": null,
                    "explore": "No",
                    "excerptContent": "",
                    "content": "<div style=\"text-align: justify; \">Discover Tata Technologies Limited Pre IPO Shares, Unlisted and De-listed Shares Stocks before buying, selling, or Investing - Check our Research report and video on Tata Technologies Limited for news and estimated returns.</div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify; \"><b>About the Company:</b></div><div style=\"text-align: justify; \">Tata Technologies Limited is a subsidiary of Tata Motors founded in 1989 headquartered in Singapore, with regional headquarters in the United States. Tata Technologies provides services in engineering and design, product development and IT services management to automotive and aerospace original equipment manufacturers and their suppliers.</div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify;\">Strengths of the Company:</div><div style=\"text-align: justify;\">1. Tata Technologies leadership team is comprised of a diverse team of globally recognized executives with a combined business experience of 200+ years.</div><div style=\"text-align: justify;\">2. The company's leadership team guides an organization of over 8,500 professionals.</div><div style=\"text-align: justify;\">3. The company has inked a pact with China's FutureMove Automotive to develop connected mobility solutions for</div><div style=\"text-align: justify;\">automotive manufacturers in China.</div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify;\">Financials of the Company:</div><div style=\"text-align: justify;\">1. Total Assets of the company have been increasing with a CAGR of 3.3%.</div><div style=\"text-align: justify;\">2. Operating Revenue has been increasing with a CAGR of 2.5%.</div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify;\">Promoters:</div><div style=\"text-align: justify;\">Top shareholder of the company is Tata Motors which hold around 70% of the shares of Tata Technologies.</div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify;\">Check the complete Research Report on Tata Technologies and keep yourself updated on latest News on Tata Technologies at:</div><div style=\"text-align: justify;\">https://www.planify.in/tata-technologies-limited/</div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify;\"><b>For more information Contact us at:</b></div><div style=\"text-align: justify;\">+91 706 55 60002</div><div style=\"text-align: justify;\">+91 706 55 60011</div><div style=\"text-align: justify;\">or e-mail us at <a href=\"help@planify.in\" target=\"_blank\">help@planify.in</a></div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify;\">Click here to subscribe to our YouTube Channel &amp; Get More Stock Market Investment Tips:</div><div style=\"text-align: justify;\">http://bit.ly/2W0LMkp</div><div style=\"text-align: justify;\"><br></div><div style=\"text-align: justify;\"><b>Our Services:</b></div><div style=\"text-align: justify;\">-Pre IPO's</div><div style=\"text-align: justify;\">-ESOP</div><div style=\"text-align: justify;\">-Investment Banking</div><div style=\"text-align: justify;\">-Pitch deck &amp; Fund Raising for Start-ups</div><div style=\"text-align: justify; \">-Life, Health, Car &amp; General Insurance</div>",
                    "blogImage": "https://testing-planify.s3.amazonaws.com/media/blog/images/Tata_technologies.jpg",
                    "blogVideo": null,
                    "videoLink": "qU4BTng4-TI",
                    "releasedDate": "2020-03-19",
                    "publish": "2021-07-05T17:52:19+05:30",
                    "created": "2021-07-05T17:52:19.811062+05:30",
                    "updated": "2022-09-19T22:36:25.879834+05:30",
                    "status": "Draft",
                    "showinpitch": true,
                    "showinhead": false,
                    "author": null,
                    "category": [],
                    "subCategory": [],
                    "relatedResearchReports": [
                        61
                    ]
                }
            ],
            "stockInvestmentChecklist": [
                {
                    "id": 48,
                    "rating": 3,
                    "accumulationRangeDescriptionFrom": 44,
                    "accumulationRangeDescriptionTo": 4,
                    "publish": "2022-09-19T22:44:53+05:30",
                    "created": "2022-09-19T22:45:52.258616+05:30",
                    "updated": "2022-09-19T22:45:52.258629+05:30",
                    "status": "published",
                    "stockProfileName": 61,
                    "analyst": 366,
                    "verifiedBy": 4,
                    "management": 1,
                    "acountingPratice": 3,
                    "profitability": 1,
                    "solvency": 1,
                    "growth": 1,
                    "valuation": 5,
                    "businessType": 2,
                    "recommendation": 7
                }
            ],
            "stockOwnershipDirector": [
                {
                    "id": 178,
                    "directorName": "rsvsvsvs",
                    "gender": "male",
                    "directorTitle": null,
                    "delta": "test for delta addition",
                    "directorImage": null,
                    "directorImageAlt": null,
                    "publish": "2022-09-12T12:37:48.017263+05:30",
                    "created": "2022-09-12T12:37:48.017644+05:30",
                    "updated": "2022-09-12T12:37:48.017653+05:30",
                    "status": "draft",
                    "stockProfileName": 61,
                    "analyst": null,
                    "verifiedBy": null
                }
            ],
            "deck": [
                {
                    "id": 13,
                    "dec_description": "this a test deck api test 1",
                    "dec_ppt": "https://testing-planify.s3.amazonaws.com/media/stock/images/deck/samplepptx_8uIQqTY.pptx",
                    "stockProfileName": 61
                },
                {
                    "id": 14,
                    "dec_description": "this a test deck api test 1",
                    "dec_ppt": "https://testing-planify.s3.amazonaws.com/media/stock/images/deck/samplepptx_jz2yvq4.pptx",
                    "stockProfileName": 61
                },
                {
                    "id": 15,
                    "dec_description": "this a test deck api test 1",
                    "dec_ppt": "https://testing-planify.s3.amazonaws.com/media/stock/images/deck/samplepptx_EmSiDih.pptx",
                    "stockProfileName": 61
                }
            ],
            "deck_images": [
                {
                    "id": 11,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 13
                },
                {
                    "id": 12,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 13
                },
                {
                    "id": 13,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 13
                },
                {
                    "id": 14,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 13
                },
                {
                    "id": 15,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 13
                },
                {
                    "id": 16,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 14
                },
                {
                    "id": 17,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 14
                },
                {
                    "id": 18,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 14
                },
                {
                    "id": 19,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": null,
                    "deck_id": 14
                },
                {
                    "id": 20,
                    "page_description": null,
                    "tag": null,
                    "page_image": null,
                    "deck_id": 14
                },
                {
                    "id": 21,
                    "page_description": null,
                    "tag": null,
                    "page_image": null,
                    "deck_id": 13
                },
                {
                    "id": 22,
                    "page_description": "this is the first image",
                    "tag": "investor",
                    "page_image": "https://testing-planify.s3.amazonaws.com/media/stock/images/image/images2_O9eYUm1.jpeg",
                    "deck_id": 13
                }
            ]
        }
        response_dict = {}
        stock_detail = {}
        stock_detail['highlights'] = {'label': 'Highlights', 'data': {}, 'child': {}}
        if highLights_data and highLights_data != []:
            stock_detail['highlights']['data']['highlights'] = highLights_data

        if stock_detail['highlights']['data'] == {} and stock_detail['highlights']['child'] == {}:
            stock_detail.pop('highlights')

        stockInvestmentChecklist_data[0]['recommendation'] = get_object_or_404(recommendationOptions,
                                                                               id=stockInvestmentChecklist_data[0][
                                                                                   'recommendation']).name
        stockInvestmentChecklist_data[0]['businessType'] = get_object_or_404(businessTypeOptions,
                                                                             id=stockInvestmentChecklist_data[0][
                                                                                 'businessType']).name
        stock_detail['stockInvestmentChecklist'] = {'label': 'Business Rating', 'data': {}, 'child': {}}
        if stockInvestmentChecklist_data and stockInvestmentChecklist_data != []:
            stock_detail['stockInvestmentChecklist']['data']['stockInvestmentChecklist'] = stockInvestmentChecklist_data

        if stock_detail['stockInvestmentChecklist']['data'] == {} and stock_detail['stockInvestmentChecklist'][
            'child'] == {}:
            stock_detail.pop('stockInvestmentChecklist')

        stock_detail['stockOwnershipDirector'] = {'label': 'Our Team', 'data': {}, 'child': {}}
        if stockOwnershipDirector_data and stockOwnershipDirector_data != []:
            stock_detail['stockOwnershipDirector']['data']['stockOwnershipDirector'] = stockOwnershipDirector_data

        if stock_detail['stockOwnershipDirector']['data'] == {} and stock_detail['stockOwnershipDirector'][
            'child'] == {}:
            stock_detail.pop('stockOwnershipDirector')

        stock_detail['newsVideospitch'] = {'label': 'Pitch', 'data': {}, 'child': {}}
        if newsVideospitch_list and newsVideospitch_list != []:
            stock_detail['newsVideospitch']['data']['newsVideospitch'] = newsVideospitch_list

        if stock_detail['newsVideospitch']['data'] == {} and stock_detail['newsVideospitch']['child'] == {}:
            stock_detail.pop('newsVideospitch')

        stock_detail['investors'] = {'label': 'Investors', 'data': {}, 'child': {}}
        if deck_data and deck_data != []:
            stock_detail['investors']['data']['deck'] = deck_data

        if deckimages_data and deckimages_data != []:
            stock_detail['investors']['data']['deckimages_data'] = deckimages_data

        if stock_detail['investors']['data'] == {} and stock_detail['investors']['child'] == {}:
            stock_detail.pop('investors')

        # response_dict.update({'stock': stock_detail})
        return Response(stock_detail)
    # return Response(context)


@api_view(['GET'])
def financialViewapi_01(request, slug):
    if request.method == 'GET':
        nav = request.GET.get('nav')
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = ""
        if stock:
            stock_detail = StockSerializer(stock)
            stock_detail = stock_detail.data
        if stock.status == 'draft' and not request.user.is_staff:
            return redirect('websiteApp:buypreIPOUrl')

        renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
        if renderBankNBFCsTemplates:
            return redirect("stockApp:financialForBankNBFCsApi", slug, nav)

        includeFile = 'UI/financialProfitAndLoss.html'
        activeNavTab = request.GET.get('nav')
        if activeNavTab:
            if activeNavTab == 'profit-and-loss':
                includeFile = 'UI/financialProfitAndLoss.html'
            elif activeNavTab == 'cash-flow':
                includeFile = 'UI/financialCashFlow.html'
            elif activeNavTab == 'balance-sheet':
                includeFile = 'UI/financialBalanceSheet.html'
        fallBackFile = 'UI/financialProfitAndLoss.html'
        tempToInclude = select_template([includeFile, fallBackFile])
        despositoryOptions, saleType = rightSideMenuObjs_serialized()

        financialStatementsFrProfitAndLossInst_list = []
        financialStatementsFrProfitAndLossInst = financialStatementsFrProfitAndLoss.objects.filter(
            stockProfileName=stock)
        if financialStatementsFrProfitAndLossInst:
            for each in financialStatementsFrProfitAndLossInst:
                financialStatementsFrProfitAndLossInst_ser = financialStatementsFrProfitAndLossSerializer(each)
                financialStatementsFrProfitAndLossInst_list.append(financialStatementsFrProfitAndLossInst_ser.data)

        financialStatementsFrBalanceSheetInst_list = []
        financialStatementsFrBalanceSheetInst = financialStatementsFrBalanceSheet.objects.filter(stockProfileName=stock)
        if financialStatementsFrBalanceSheetInst:
            for each in financialStatementsFrBalanceSheetInst:
                financialStatementsFrBalanceSheetInst_ser = financialStatementsFrBalanceSheetSerializer(each)
                financialStatementsFrBalanceSheetInst_list.append(financialStatementsFrBalanceSheetInst_ser.data)

        financialStatementsFrCashFlowInst_list = []
        financialStatementsFrCashFlowInst = financialStatementsFrCashFlow.objects.filter(stockProfileName=stock)
        if financialStatementsFrCashFlowInst:
            for each in financialStatementsFrCashFlowInst:
                financialStatementsFrCashFlowInst_ser = financialStatementsFrCashFlowSerializer(each)
                financialStatementsFrCashFlowInst_list.append(financialStatementsFrCashFlowInst_ser.data)

        financialCompanyUpdatesInst_list = []
        financialCompanyUpdatesInst = financialCompanyUpdates.objects.filter(stockProfileName=stock).order_by('title')
        if financialCompanyUpdatesInst:
            for each in financialCompanyUpdatesInst:
                # print(each.linkFrReport)
                financialCompanyUpdatesInst_ser = financialCompanyUpdatesSerializer(each)  # .data
                # financialCompanyUpdatesInst_ser['linkFrReport'] = each.linkFrReport
                financialCompanyUpdatesInst_list.append(financialCompanyUpdatesInst_ser.data)

        stockProfitAndLossInst_list = []
        stockProfitAndLossInst = stockProfitAndLoss.objects.filter(stockProfileName=stock).order_by('year')
        if len(stockProfitAndLossInst):
            for each in stockProfitAndLossInst:
                stockProfitAndLossInst_ser = stockProfitAndLossSerializer(each)
                stockProfitAndLossInst_list.append(stockProfitAndLossInst_ser.data)

        stockBalanceSheetInst_list = []
        stockBalanceSheetInst = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('year')
        if stockBalanceSheetInst:
            for each in stockBalanceSheetInst:
                stockBalanceSheetInst_ser = stockBalanceSheetSerializer(each)
                stockBalanceSheetInst_list.append(stockBalanceSheetInst_ser.data)

        stockCashFlowInst_list = []
        stockCashFlowInst = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')
        if stockCashFlowInst:
            for each in stockCashFlowInst:
                stockCashFlowInst_ser = stockCashFlowSerializer(each)
                stockCashFlowInst_list.append(stockCashFlowInst_ser.data)

        stockDeckAndDocsInst_list = []
        stockDeckAndDocsInst = stockDeckAndDocs.objects.filter(stockProfileName=stock).order_by('-id')
        if stockCashFlowInst:
            for each in stockDeckAndDocsInst:
                stockDeckAndDocsInst_ser = stockDeckAndDocsSerializer(each)
                stockDeckAndDocsInst_list.append(stockDeckAndDocsInst_ser.data)

        figureUnitInst_list = ""
        try:
            figureUnitInst = get_object_or_404(financialFigureUnits, stockProfileName=stock)
            if figureUnitInst:
                figureUnitInst_detail = financialFigureUnitsSerializer(figureUnitInst)
                figureUnitInst_detail = figureUnitInst_detail.data
        except:
            figureUnitInst = None

        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
        except:
            stockAdmInst = None

        annualReportsDHRPInst_list = []
        try:
            annualReportsDHRPInst = annualReportsDHRP.objects.filter(stockProfileName=stock)
            if annualReportsDHRPInst:
                for each in annualReportsDHRPInst:
                    annualReportsDHRPInst_ser = annualReportsDHRPSerializer(each)
                    annualReportsDHRPInst_list.append(annualReportsDHRPInst_ser.data)
        except:
            annualReportsDHRPInst = None

        balanceSheetTTMInst_detail = ""
        try:
            balanceSheetTTMInst = stockBalanceSheetTTM.objects.get(stockProfileName=stock)
            if balanceSheetTTMInst:
                balanceSheetTTMInst_detail = stockBalanceSheetTTMSerializer(balanceSheetTTMInst)
                balanceSheetTTMInst_detail = balanceSheetTTMInst_detail.data
                balanceSheetTTMInst_detail['year'] = str(balanceSheetTTMInst_detail['year'] + 1) + " *"
        except:
            balanceSheetTTMInst = None

        profitAndLossTTMInst_detail = ""
        try:
            profitAndLossTTMInst = stockProfitAndLossTTM.objects.get(stockProfileName=stock)
            if profitAndLossTTMInst:
                profitAndLossTTMInst_detail = stockProfitAndLossTTMSerializer(profitAndLossTTMInst)
                profitAndLossTTMInst_detail = profitAndLossTTMInst_detail.data
                profitAndLossTTMInst_detail['year'] = str(profitAndLossTTMInst_detail['year'] + 1) + " *"
        except:
            profitAndLossTTMInst = None

        cashFlowTTMInst_detail = ""
        try:
            cashFlowTTMInst = stockCashFlowTTM.objects.get(stockProfileName=stock)
            if cashFlowTTMInst:
                cashFlowTTMInst_detail = stockCashFlowTTMSerializer(cashFlowTTMInst)
                cashFlowTTMInst_detail = cashFlowTTMInst_detail.data
                cashFlowTTMInst_detail['year'] = str(cashFlowTTMInst_detail['year'] + 1) + " *"
        except:
            cashFlowTTMInst = None

        # description field for SEO - starts
        stockFinBalanceSheetSEOInst_detail = ""
        try:
            stockFinBalanceSheetSEOInst = stockFinBalanceSheetSEO.objects.get(stockProfileName=stock)
            if stockFinBalanceSheetSEOInst:
                stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOSerializer(stockFinBalanceSheetSEOInst)
                stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOInst_detail.data
        except:
            stockFinBalanceSheetSEOInst = None
        # description field for SEO - ends

        # Description
        if stockFinBalanceSheetSEOInst:
            balanceSheetDescriptionSEO = stockFinBalanceSheetSEOInst.balanceSheetDescriptionSEO
            profitAndLossDescriptionSEO = stockFinBalanceSheetSEOInst.profitAndLossDescriptionSEO
            cashFlowDescriptionSEO = stockFinBalanceSheetSEOInst.cashFlowDescriptionSEO
        else:
            balanceSheetDescriptionSEO = None
            profitAndLossDescriptionSEO = None
            cashFlowDescriptionSEO = None

        if figureUnitInst:
            shareOutstandingNumber = figureUnitInst.shareOutstandingNumber
            financialNumbers = figureUnitInst.financialNumbers
        else:
            shareOutstandingNumber = None
            financialNumbers = None

        response_dict = {}
        normal_mapping, nbfc_mapping = financial_mapping()
        if nav == 'cash-flow':
            response_dict['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle,
                                          'description': cashFlowDescriptionSEO,
                                          'shareOutstandingNumbers': shareOutstandingNumber,
                                          'financialNumbers': financialNumbers}
            response_dict['Rationals'] = {'label': 'Rationals', 'data': financialStatementsFrCashFlowInst_list,
                                          'child': {}}
            response_dict['Financials'] = {'label': 'Financials', 'data': {'tableData': stockCashFlowInst_list,
                                                                           'TTMData': cashFlowTTMInst_detail},
                                           'child': {}}

        elif nav == 'balance-sheet':
            response_dict['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle,
                                          'description': balanceSheetDescriptionSEO,
                                          'shareOutstandingNumbers': shareOutstandingNumber,
                                          'financialNumbers': financialNumbers}
            response_dict['Rationals'] = {'label': 'Rationals', 'data': financialStatementsFrBalanceSheetInst_list,
                                          'child': {}}
            response_dict['Financials'] = {'label': 'Financials', 'data': {'tableData': stockBalanceSheetInst_list,
                                                                           'TTMData': balanceSheetTTMInst_detail},
                                           'child': {}}

        else:
            response_dict['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle,
                                          'description': profitAndLossDescriptionSEO,
                                          'shareOutstandingNumbers': shareOutstandingNumber,
                                          'financialNumbers': financialNumbers}
            response_dict['Rationals'] = {'label': 'Rationals', 'data': financialStatementsFrProfitAndLossInst_list,
                                          'child': {}}
            response_dict['Financials'] = {'label': 'Financials', 'data': {'tableData': stockProfitAndLossInst_list,
                                                                           'TTMData': profitAndLossTTMInst_detail},
                                           'child': {}}

        response_dict['Annual Reports'] = {'label': 'Annual Reports', 'data': financialCompanyUpdatesInst_list,
                                           'child': {}}
        response_dict['Decks & Infographics'] = {'label': 'Decks & Infographics', 'data': stockDeckAndDocsInst_list,
                                                 'child': {}}
        response_dict['DRHP'] = {'label': 'DRHP', 'data': annualReportsDHRPInst_list, 'child': {}}

        return Response({'response': response_dict})


@api_view(['GET'])
def getFinancialForBankNBFCsView_01(request, slug, nav):
    response_dict = {}
    if not nav:
        nav = request.GET.get('nav')
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock)
        stock_detail = stock_detail.data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    includeFile = 'UI/financialProfitAndLossForBankNBFCs.html'
    activeNavTab = request.GET.get('nav')
    if activeNavTab:
        if activeNavTab == 'profit-and-loss':
            includeFile = 'UI/financialProfitAndLossForBankNBFCs.html'
        elif activeNavTab == 'cash-flow':
            includeFile = 'UI/financialCashFlow.html'
        elif activeNavTab == 'balance-sheet':
            includeFile = 'UI/financialBalanceSheetForBankNBFCs.html'
    fallBackFile = 'UI/financialProfitAndLossForBankNBFCs.html'
    tempToInclude = select_template([includeFile, fallBackFile])
    despositoryOptions, saleType = rightSideMenuObjs()

    stockTransferDepositoryOptions_list = []
    try:
        if despositoryOptions:
            for each in despositoryOptions:
                stockTransferDepositoryOptions_ser = stockTransferDepositoryOptionsSerializer(each)
                stockTransferDepositoryOptions_list.append(stockTransferDepositoryOptions_ser.data)
    except:
        despositoryOptions = None
        stockTransferDepositoryOptions_list = []

    saleTypeOptions_list = []
    try:
        if saleType:
            for each in saleType:
                saleTypeOptions_ser = saleTypeOptionsSerializer(each)
                saleTypeOptions_list.append(saleTypeOptions_ser.data)
    except:
        saleType = None
        saleTypeOptions_list = []

    financialStatementsFrProfitAndLossInst_list = []
    financialStatementsFrProfitAndLossInst = financialStatementsFrProfitAndLoss.objects.filter(stockProfileName=stock)
    if financialStatementsFrProfitAndLossInst:
        for each in financialStatementsFrProfitAndLossInst:
            financialStatementsFrProfitAndLossInst_ser = financialStatementsFrProfitAndLossSerializer(each)
            financialStatementsFrProfitAndLossInst_list.append(financialStatementsFrProfitAndLossInst_ser.data)

    # createFinancialStatementsFrProfitAndLoss = financialStatementsFrProfitAndLossForm()

    financialStatementsFrBalanceSheetInst_list = []
    financialStatementsFrBalanceSheetInst = financialStatementsFrBalanceSheet.objects.filter(stockProfileName=stock)
    if financialStatementsFrBalanceSheetInst:
        for each in financialStatementsFrBalanceSheetInst:
            financialStatementsFrBalanceSheetInst_ser = financialStatementsFrBalanceSheetSerializer(each)
            financialStatementsFrBalanceSheetInst_list.append(financialStatementsFrBalanceSheetInst_ser.data)
    # createFinancialStatementsFrBalanceSheet = financialStatementsFrBalanceSheetForm()

    financialStatementsFrCashFlowInst_list = []
    financialStatementsFrCashFlowInst = financialStatementsFrCashFlow.objects.filter(stockProfileName=stock)
    if financialStatementsFrCashFlowInst:
        for each in financialStatementsFrCashFlowInst:
            financialStatementsFrCashFlowInst_ser = financialStatementsFrCashFlowSerializer(each)
            financialStatementsFrCashFlowInst_list.append(financialStatementsFrCashFlowInst_ser.data)
    # createFinancialStatementsFrCashFlow = financialStatementsFrCashFlowForm()

    financialCompanyUpdatesInst_list = []
    financialCompanyUpdatesInst = financialCompanyUpdates.objects.filter(stockProfileName=stock).order_by('title')
    if financialCompanyUpdatesInst:
        for each in financialCompanyUpdatesInst:
            # print(each.linkFrReport)
            financialCompanyUpdatesInst_ser = financialCompanyUpdatesSerializer(each)  # .data
            # financialCompanyUpdatesInst_ser['linkFrReport'] = each.linkFrReport
            financialCompanyUpdatesInst_list.append(financialCompanyUpdatesInst_ser.data)
    # createFinancialCompanyUpdates = financialCompanyUpdatesForm()

    stockProfitAndLossInst_list = []
    stockProfitAndLossInst = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
    if len(stockProfitAndLossInst):
        for each in stockProfitAndLossInst:
            stockProfitAndLossInst_ser = stockProfitAndLossBankNBFCSerializer(each)
            stockProfitAndLossInst_list.append(stockProfitAndLossInst_ser.data)

    # createstockProfitAndLoss = stockProfitAndLossBankNBFCForm()

    stockBalanceSheetInst_list = []
    stockBalanceSheetInst = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('year')
    if stockBalanceSheetInst:
        for each in stockBalanceSheetInst:
            stockBalanceSheetInst_ser = stockBalanceSheetBankNBFCSerializer(each)
            stockBalanceSheetInst_list.append(stockBalanceSheetInst_ser.data)
    # createStockBalanceSheet = stockBalanceSheetBankNBFCForm()

    stockCashFlowInst_list = []
    stockCashFlowInst = stockCashFlow.objects.filter(stockProfileName=stock).order_by('year')
    if stockCashFlowInst:
        for each in stockCashFlowInst:
            stockCashFlowInst_ser = stockCashFlowSerializer(each)
            stockCashFlowInst_list.append(stockCashFlowInst_ser.data)

    # createStockCashFlow = stockCashFlowForm()
    figureUnitInst_detail = ""
    try:
        figureUnitInst = get_object_or_404(financialFigureUnits, stockProfileName=stock)
        if figureUnitInst:
            figureUnitInst_detail = financialFigureUnitsSerializer(figureUnitInst)
            figureUnitInst_detail = figureUnitInst_detail.data
    except:
        figureUnitInst = None
        figureUnitInst_detail = ""
    # financialFigureUnitsCreate = financialFigureUnitsForm()

    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
            stockAdmInst_detail = stockAdmInst_detail.data
    except:
        stockAdmInst = None
        stockAdmInst_detail = ""

    annualReportsDHRPInst_list = []
    try:
        annualReportsDHRPInst = annualReportsDHRP.objects.filter(stockProfileName=stock)
        if annualReportsDHRPInst:
            for each in annualReportsDHRPInst:
                annualReportsDHRPInst_ser = annualReportsDHRPSerializer(each)
                annualReportsDHRPInst_list.append(annualReportsDHRPInst_ser.data)
    except:
        annualReportsDHRPInst = None
    # createAnnualReportsDHRP = annualReportsDHRPForm(instance=annualReportsDHRPInst)

    BalanceSheetBankNBFCTTMInst_detail = ""
    try:
        stockBalanceSheetBankNBFCTTMInst = stockBalanceSheetBankNBFCTTM.objects.get(stockProfileName=stock)
        if stockBalanceSheetBankNBFCTTMInst:
            BalanceSheetBankNBFCTTMInst_detail = stockBalanceSheetBankNBFCTTMSerializer(
                stockBalanceSheetBankNBFCTTMInst)
            BalanceSheetBankNBFCTTMInst_detail = BalanceSheetBankNBFCTTMInst_detail.data
            BalanceSheetBankNBFCTTMInst_detail['year'] = str(BalanceSheetBankNBFCTTMInst_detail['year'] + 1) + " *"
    except:
        stockBalanceSheetBankNBFCTTMInst = None
        BalanceSheetBankNBFCTTMInst_detail = ""

    # createStockBalanceSheetBankNBFCTTM = stockBalanceSheetBankNBFCTTMForm(instance=stockBalanceSheetBankNBFCTTMInst)

    ProfitAndLossBankNBFCTTMInst_detail = ""
    try:
        stockProfitAndLossBankNBFCTTMInst = stockProfitAndLossBankNBFCTTM.objects.get(stockProfileName=stock)
        if stockProfitAndLossBankNBFCTTMInst:
            ProfitAndLossBankNBFCTTMInst_detail = stockProfitAndLossBankNBFCTTMSerializer(
                stockProfitAndLossBankNBFCTTMInst)
            ProfitAndLossBankNBFCTTMInst_detail = ProfitAndLossBankNBFCTTMInst_detail.data
            ProfitAndLossBankNBFCTTMInst_detail['year'] = str(ProfitAndLossBankNBFCTTMInst_detail['year'] + 1) + " *"
    except:
        stockProfitAndLossBankNBFCTTMInst = None
        ProfitAndLossBankNBFCTTMInst_detail = ""

    # createStockProfitAndLossBankNBFCTTM = stockProfitAndLossBankNBFCTTMForm(instance=stockProfitAndLossBankNBFCTTMInst)

    cashFlowTTMInst_detail = ""
    try:
        cashFlowTTMInst = stockCashFlowTTM.objects.get(stockProfileName=stock)
        if cashFlowTTMInst:
            cashFlowTTMInst_detail = stockCashFlowTTMSerializer(cashFlowTTMInst)
            cashFlowTTMInst_detail = cashFlowTTMInst_detail.data
            cashFlowTTMInst_detail['year'] = str(cashFlowTTMInst_detail['year'] + 1) + " *"
    except:
        cashFlowTTMInst = None
        cashFlowTTMInst_detail = ""
    # createCashFlowTTM = stockCashFlowTTMForm(instance=cashFlowTTMInst)

    # description field for SEO - starts
    stockFinBalanceSheetSEOInst_detail = ""
    try:
        stockFinBalanceSheetSEOInst = stockFinBalanceSheetSEO.objects.get(stockProfileName=stock)
        if stockFinBalanceSheetSEOInst:
            stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOSerializer(stockFinBalanceSheetSEOInst)
            stockFinBalanceSheetSEOInst_detail = stockFinBalanceSheetSEOInst_detail.data
    except:
        stockFinBalanceSheetSEOInst = None
        stockFinBalanceSheetSEOInst_detail = ""
    # createStockFinBalanceSheetSEO = stockFinBalanceSheetSEOForm(instance=stockFinBalanceSheetSEOInst)
    # description field for SEO - ends

    stockDeckAndDocsInst_list = []
    stockDeckAndDocsInst = stockDeckAndDocs.objects.filter(stockProfileName=stock).order_by('-id')
    if stockDeckAndDocsInst:
        for each in stockDeckAndDocsInst:
            stockDeckAndDocsInst_ser = stockDeckAndDocsSerializer(each)
            stockDeckAndDocsInst_list.append(stockDeckAndDocsInst_ser.data)
    # stockDeckAndDocsInstForm = stockDeckAndDocsForm()

    # Description
    if stockFinBalanceSheetSEOInst:
        balanceSheetDescriptionSEO = stockFinBalanceSheetSEOInst.balanceSheetDescriptionSEO
        profitAndLossDescriptionSEO = stockFinBalanceSheetSEOInst.profitAndLossDescriptionSEO
        cashFlowDescriptionSEO = stockFinBalanceSheetSEOInst.cashFlowDescriptionSEO
    else:
        balanceSheetDescriptionSEO = None
        profitAndLossDescriptionSEO = None
        cashFlowDescriptionSEO = None

    if figureUnitInst:
        shareOutstandingNumber = figureUnitInst.shareOutstandingNumber
        financialNumbers = figureUnitInst.financialNumbers
    else:
        shareOutstandingNumber = None
        financialNumbers = None
    normal_mapping, nbfc_mapping = financial_mapping()
    response_dict = {}

    if nav == 'cash-flow':
        response_dict['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle,
                                      'description': cashFlowDescriptionSEO,
                                      'shareOutstandingNumbers': shareOutstandingNumber,
                                      'financialNumbers': financialNumbers}
        response_dict['Rationals'] = {'label': 'Rationals', 'data': financialStatementsFrCashFlowInst_list, 'child': {}}
        response_dict['Financials'] = {'label': 'Financials',
                                       'data': {'tableData': stockCashFlowInst_list, 'TTMData': cashFlowTTMInst_detail},
                                       'child': {}}

    elif nav == 'balance-sheet':
        response_dict['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle,
                                      'description': balanceSheetDescriptionSEO,
                                      'shareOutstandingNumbers': shareOutstandingNumber,
                                      'financialNumbers': financialNumbers}
        response_dict['Rationals'] = {'label': 'Rationals', 'data': financialStatementsFrBalanceSheetInst_list,
                                      'child': {}}
        response_dict['Financials'] = {'label': 'Financials', 'data': {'tableData': stockBalanceSheetInst_list,
                                                                       'TTMData': BalanceSheetBankNBFCTTMInst_detail},
                                       'child': {}}

    else:
        response_dict['extraData'] = {'stockName': stock.stockName, 'seoTitle': stock.seoTitle,
                                      'description': profitAndLossDescriptionSEO,
                                      'shareOutstandingNumbers': shareOutstandingNumber,
                                      'financialNumbers': financialNumbers}
        response_dict['Rationals'] = {'label': 'Rationals', 'data': financialStatementsFrProfitAndLossInst_list,
                                      'child': {}}
        response_dict['Financials'] = {'label': 'Financials', 'data': {'tableData': stockProfitAndLossInst_list,
                                                                       'TTMData': ProfitAndLossBankNBFCTTMInst_detail},
                                       'child': {}}

    response_dict['Annual Reports'] = {'label': 'Annual Reports', 'data': financialCompanyUpdatesInst_list, 'child': {}}
    response_dict['Decks & Infographics'] = {'label': 'Decks & Infographics', 'data': stockDeckAndDocsInst_list,
                                             'child': {}}
    response_dict['DRHP'] = {'label': 'DRHP', 'data': annualReportsDHRPInst_list, 'child': {}}

    return Response({'response': response_dict})


@api_view(['GET'])
def searchStockApi(request):
    query = request.GET.get('stockName')
    query_cat = request.GET.getlist('categoryId')
    load_categories = request.GET.get('categories')
    stockList_new = []
    if load_categories:
        categories_list = []
        categories = categoryOptions.objects.all()
        if categories:
            for each in categories:
                categories_list.append(
                    {'Id': each.id, 'name': each.name, 'shortForm': each.shortForm, 'fullForm': each.fullForm})

        context = {
            'categories': categories_list,
            'query': 'all',
        }
        return Response(context)

    if query:
        stockList = stockBasicDetail.objects.filter(Q(stockName__icontains=query)).distinct()
        if stockList:
            for each in stockList:
                # tmp = StockSerializer(each).data
                stockList_new.append({'stockId': each.id, 'stockName': each.stockName})

        context = {
            'stockList': stockList_new,
            'query': query,
        }
        return Response(context)

    if query_cat:
        stockEssentialsList = stockEssentials.objects.filter(category__in=query_cat).distinct()
        if stockEssentialsList:
            for each in stockEssentialsList:
                # tmp = StockSerializer(each).data
                stockList_new.append(
                    {'stockId': each.stockProfileName.id, 'stockName': each.stockProfileName.stockName})

        context = {
            'stockList': stockList_new,
            'query_category': query_cat,
        }
        return Response(context)
    return Response({'detail': 'not found'})


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def campaignApi(request):
    id = request.data.get('id')
    stock_id = request.data.get('stockProfileName')

    if request.method == 'DELETE':
        if id:
            response = campaign.objects.filter(id=id)
            if response:
                response.delete()
                return Response({
                    'msg': 'Data Deleted Successfully'
                })
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
    if request.method == 'PUT':
        if id:
            try:
                response = campaign.objects.get(id=id)

                if response:
                    request.POST._mutable = True
                    myrequest = request.data
                    serializer = campaignSerializer(response).data

                    myrequest['stockProfileName'] = serializer['stockProfileName']  # stock.id
                    if 'endDate' not in myrequest:
                        myrequest['endDate'] = serializer['endDate']
                    if 'startDate' not in myrequest:
                        myrequest['startDate'] = serializer['startDate']
                    serializer = campaignSerializer(response, data=myrequest)
                    serializer_checker = serializer_valid(serializer)
                    return Response(serializer_checker)
                else:
                    return Response({
                        'msg': 'Please Enter Valid Id'
                    })
            except:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'Id Filed Required'
            })

    if request.method == 'GET':
        if id:
            response = campaign.objects.filter(id=id)
            if response:
                serializer = campaignSerializer(response)
                return Response(serializer.data)
            else:
                return Response({
                    'msg': 'Please Enter Valid Id'
                })
        else:
            return Response({
                'msg': 'Please Provide Id'
            })
    if request.method == 'POST':
        # return Response({'stock_id': stock_id})
        resp = []
        stock_id = list(map(int, stock_id.split(',')))
        for item in stock_id:
            similar_stock_campaign = campaign.objects.filter(stockProfileName=item)
            if len(similar_stock_campaign):
                return Response({
                    'msg': 'Campaign for this stock already exists'
                })
            stock = get_object_or_404(stockBasicDetail, id=item)
            request.POST._mutable = True
            myrequest = request.data
            # print(type(myrequest['stockProfileName']))
            myrequest['stockProfileName'] = stock.id
            campaign_serializer = campaignSerializer(data=myrequest)
            if campaign_serializer.is_valid():
                campaign_serializer.save()
                resp.append(campaign_serializer.data)
            else:
                return JsonResponse(campaign_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # response = campaign.objects.filter(stockProfileName_id=stock.id)
            # serializer = campaignSerializer(response, many=True)

        return Response(resp, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getCampaignsApi(request):
    #if request.user.is_staff:
        name_string = request.GET.get('stockName')
        activeFlag = request.GET.get('activeFlag')
        completeFlag = request.GET.get('completeFlag')
        date1 = request.GET.get('startDate')
        date2 = request.GET.get('endDate')
        itemCount = request.GET.get('itemCount')
        activeFlag_bool = True if activeFlag == 'true' else False
        campaigns = campaign.objects.filter(Q(stockProfileName__stockName__icontains=name_string))
        if activeFlag:
            campaigns = campaigns.filter(isActive=activeFlag_bool)
        if completeFlag:
            now = datetime.datetime.now()
            campaigns = campaigns.filter(Q(endDate__lt=now))
        if date1 and date2:
            date1 = datetime.datetime.strptime(date1.replace('T', ' ').replace('Z', ''), "%Y-%m-%d %H:%M:%S")
            date2 = datetime.datetime.strptime(date2.replace('T', ' ').replace('Z', ''), "%Y-%m-%d %H:%M:%S")
            campaigns = campaigns.filter(Q(startDate__range=(date1, date2)) | Q(endDate__range=(date1, date2)))

        paginator = Paginator(campaigns, per_page=int(itemCount))
        page = int(request.GET.get('page'))
        try:
            campaigns = paginator.page(page)
        except PageNotAnInteger:
            campaigns = paginator.page(1)
        except EmptyPage:
            campaigns = paginator.page(paginator.num_pages)
        flag = 'campaignListing'
        totalPages = paginator.num_pages
        try:
            if int(page) > totalPages:
                messages.error(request, 'Invalid Page Number.')
                page = 1
                campaigns = paginator.page(page)
        except:
            pass
        # print(tot)
        # print(campaigns.object_list)

        campaigns_list = []
        # campaigns = campaign.objects.all()

        if campaigns.object_list:
            for each in campaigns.object_list:
                temp = {}
                temp['id'] = each.id
                temp['stockId'] = each.stockProfileName.id
                temp['stockName'] = each.stockProfileName.stockName
                temp['campaignDescription'] = each.campaign_description
                temp['startDate'] = each.startDate
                temp['endDate'] = each.endDate
                temp['isActive'] = each.isActive
                campaigns_list.append(temp)

        return Response({"campaigns": campaigns_list,
                        "flag": flag,
                        "page": page,
                        "totalPages": totalPages})
    #else:
    #    return Response({"message": "Operation is not permitted."})


@api_view(['GET'])
def peersViewapi_02(request, slug):
    if request.method == 'GET':
        stock = get_object_or_404(stockBasicDetail, id=slug)
        stock_detail = {}
        if stock:
            stock_detail = StockSerializer(stock)
            stock_detail = stock_detail.data
        if stock.status == 'draft' and not request.user.is_staff:
            return redirect('websiteApp:buypreIPOUrl')

        renderBankNBFCsTemplates = renderBankNBFCsTemplatesView(stock)
        if renderBankNBFCsTemplates:
            return redirect('stockApp:peersViewNBFCapi', slug)
        netProfitMarginCY = revenueCY = 0.00
        allStockList_list = []
        allStockList = stockBasicDetail.objects.all()
        if allStockList:
            for each in allStockList:
                allStockList_ser = StockSerializer(each)
                allStockList_list.append(allStockList_ser.data)
        yearCY = onlyRevenue = ebitda = None
        revenuePeersCompanyList_list = []
        revenuePeersCompanyList = peersCompanyLinking.objects.filter(stockProfileName=stock)
        if revenuePeersCompanyList:
            for each in revenuePeersCompanyList:
                revenuePeersCompanyList_ser = peersCompanyLinkingSerializer(each)
                revenuePeersCompanyList_list.append(revenuePeersCompanyList_ser.data)
        totalInvPY = totalInvCY = totalRevCY = totalIntangiblesCY = totalIntangiblesPY = totalAssetCY = totalAssetPY = netIncomeCY = totalEquityCY = totalEquityPY = EBITCY = longTermDebtCY = longTermDebtPY = 0.00
        totalAssetTurnoverRatioCY = totalFixedAssetTurnoverRatioCY = ROECY = ROCECY = debtToEquity = 0.00
        totalLngDebtCY = currPortLngTermDebtCY = currPortionLeasesCY = lngTermPortionOfLeasesCY = 0.0
        totalLngDebtPY = currPortLngTermDebtPY = currPortionLeasesPY = lngTermPortionOfLeasesPY = 0.0
        totalNonCurrentLiabilityCY = totalNonCurrentLiabilityPY = 0.0

        # revenueGraphData = {}
        screenerDict = {}
        stockAdmInst_detail = ""
        try:
            stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
            if stockAdmInst:
                stockAdmInst_detail = stockAdminSerializer(stockAdmInst)
                stockAdmInst_detail = stockAdmInst_detail.data
        except:
            stockAdmInst = None
        try:
            latestProfitAndLoss = stockProfitAndLoss.objects.filter(stockProfileName=stock).latest('year')
        except:
            latestProfitAndLoss = 0.00
        try:
            latestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).latest('year')
        except:
            latestBalanceSheet = 0.00
        try:
            secondLatestBalanceSheet = stockBalanceSheet.objects.filter(stockProfileName=stock).order_by('-year')[1:2]
        except:
            secondLatestBalanceSheet = 0.00
        cashAndShortTermBalSheet = minorityInterestVal = totalCalculatedLnDebtCY = 0
        if latestBalanceSheet:
            cashAndShortTermBalSheet = latestBalanceSheet.cashAndShortTermInvestments
            minorityInterestVal = latestBalanceSheet.minorityInterest
            for item in secondLatestBalanceSheet:
                if item:
                    if latestProfitAndLoss != 0.00:
                        if latestProfitAndLoss.revenue:
                            yearCY = latestProfitAndLoss.year
                            if latestProfitAndLoss.revenue:
                                totalRevCY = Decimal(latestProfitAndLoss.revenue)
                            if latestBalanceSheet.totalInventory:
                                totalInvCY = Decimal(latestBalanceSheet.totalInventory)
                            if item.totalInventory:
                                totalInvPY = Decimal(item.totalInventory)
                            if latestBalanceSheet.otherIntangibleAssests:
                                totalIntangiblesCY = Decimal(latestBalanceSheet.otherIntangibleAssests)
                            if item.otherIntangibleAssests:
                                totalIntangiblesPY = Decimal(item.otherIntangibleAssests)
                            if latestBalanceSheet.totalAssets:
                                totalAssetCY = Decimal(latestBalanceSheet.totalAssets)
                            if item.totalAssets:
                                totalAssetPY = Decimal(item.totalAssets)
                            if latestProfitAndLoss.netIncome:
                                netIncomeCY = Decimal(latestProfitAndLoss.netIncome)
                            if latestBalanceSheet.totalEquity:
                                totalEquityCY = Decimal(latestBalanceSheet.totalEquity)
                            if item.totalEquity:
                                totalEquityPY = Decimal(item.totalEquity)
                            if latestProfitAndLoss.pbit:
                                EBITCY = Decimal(latestProfitAndLoss.pbit)
                            if latestBalanceSheet.totalLongTermDebt:
                                totalLngDebtCY = Decimal(latestBalanceSheet.totalLongTermDebt)
                            if item.totalLongTermDebt:
                                totalLngDebtPY = Decimal(item.totalLongTermDebt)
                            if latestBalanceSheet.currentPortionOfLongTermDebt:
                                currPortLngTermDebtCY = Decimal(latestBalanceSheet.currentPortionOfLongTermDebt)
                            if item.currentPortionOfLongTermDebt:
                                currPortLngTermDebtPY = Decimal(item.currentPortionOfLongTermDebt)
                            if latestBalanceSheet.currentPortionOfLeases:
                                currPortionLeasesCY = Decimal(latestBalanceSheet.currentPortionOfLeases)
                            if item.currentPortionOfLeases:
                                currPortionLeasesPY = Decimal(item.currentPortionOfLeases)
                            if latestBalanceSheet.longTermPortionOfLeases:
                                lngTermPortionOfLeasesCY = Decimal(latestBalanceSheet.longTermPortionOfLeases)
                            if item.longTermPortionOfLeases:
                                lngTermPortionOfLeasesPY = Decimal(item.longTermPortionOfLeases)
                            if latestBalanceSheet.nonCurrentLiabilities:
                                totalNonCurrentLiabilityCY = Decimal(latestBalanceSheet.nonCurrentLiabilities)
                            if item.nonCurrentLiabilities:
                                totalNonCurrentLiabilityPY = Decimal(item.nonCurrentLiabilities)

                            totalCalculatedLnDebtCY = Decimal(totalLngDebtCY) + Decimal(
                                currPortLngTermDebtCY) + Decimal(
                                currPortionLeasesCY) + Decimal(lngTermPortionOfLeasesCY)
                            totalCalculatedLnDebtPY = Decimal(totalLngDebtPY) + Decimal(
                                currPortLngTermDebtPY) + Decimal(
                                currPortionLeasesPY) + Decimal(lngTermPortionOfLeasesPY)

                            totalAssetTurnoverRatioCY = round(
                                totalAssetTurnoverRatioFormula(totalRevCY, totalAssetCY, totalAssetPY), 2)
                            totalFixedAssetTurnoverRatioCY = round(
                                totalFixedAssetTurnoverRatioFormula(totalRevCY, totalInvCY, totalInvPY), 2)
                            ROECY = round(ROEFormula(netIncomeCY, totalEquityCY, totalEquityPY), 2)
                            ROCECY = round(ROCEFormula(EBITCY, totalEquityCY, totalEquityPY, totalNonCurrentLiabilityCY,
                                                       totalNonCurrentLiabilityPY), 2)
                            debtToEquity = round(
                                debtToEquityFormula(totalCalculatedLnDebtCY, totalCalculatedLnDebtPY, totalEquityCY,
                                                    totalEquityPY), 2)
        if latestProfitAndLoss:
            if latestProfitAndLoss.totalRevenue:
                revenueCY = round(latestProfitAndLoss.totalRevenue, 2)
            if latestProfitAndLoss.revenue:
                onlyRevenue = round(latestProfitAndLoss.revenue, 2)
            if latestProfitAndLoss.ebidta:
                ebitda = round(latestProfitAndLoss.ebidta, 2)
            # changes in NPM - Peers starts (Formula changed - It should be revenue of operations insted of Total Revenue )
            netProfitMarginCY = round(
                netProfitMarginFormula(latestProfitAndLoss.netIncome, latestProfitAndLoss.revenue), 2)
        # changes in NPM - Peers ends

        peRatioCS, pbRatioCS = currentStockPEPBView(stock)
        try:
            essentialInst = stockEssentials.objects.get(stockProfileName=stock)
        except:
            essentialInst = None
        marketCapCS = marketCapView(stock)
        if onlyRevenue == 0 or onlyRevenue == None:
            onlyRevenue = 1

        marketCapBySales = return_val_or_0(marketCapCS) / return_val_or_1(onlyRevenue)

        if essentialInst:
            enterpriseValueInst = essentialInst.enterpriseValue
            balanceWithRBIVal = essentialInst.balance_with_RBI
            preferenceEquityVal = essentialInst.preference_equity
        else:
            enterpriseValueInst = 0
            balanceWithRBIVal = preferenceEquityVal = 0
        if ebitda == 0:
            ebitda = 1

        try:
            if stock.stockProfileNameFFU.financialNumbers == 'L':
                marketCapCS = numberConversion(marketCapCS, currentSystem='Cr',
                                               convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        enterpriseVal = return_val_or_0(marketCapCS) - (
                return_val_or_0(cashAndShortTermBalSheet) - return_val_or_0(balanceWithRBIVal)) + return_val_or_0(
            totalCalculatedLnDebtCY) + return_val_or_0(preferenceEquityVal) + return_val_or_0(minorityInterestVal)

        # numberConversion
        # enterpriseVal = numberConversion(enterpriseVal, currentSystem='L', convertTo=stock.stockProfileNameFFU.financialNumbers)
        evByEbitda = round(return_val_or_0(enterpriseVal) / return_val_or_1(ebitda), 2)
        # conversion

        try:
            if stock.stockProfileNameFFU.financialNumbers == 'L':
                marketCapBySales = numberConversion(marketCapBySales, currentSystem='Cr',
                                                    convertTo=stock.stockProfileNameFFU.financialNumbers)
        except:
            pass

        marketCapBySales = round(marketCapBySales, 2)

        stockname = str(stock_detail.get("stockName"))
        screenerDict = {stockname:
            {
                'id': stock.id,
                'type': 'current',
                'revenue': revenueCY,
                'netProfitMargin': netProfitMarginCY,
                'assetTurnoverRation': totalAssetTurnoverRatioCY,
                'totalFixedAssetTurnoverRatio': totalFixedAssetTurnoverRatioCY,
                'ROE': ROECY,
                'ROCE': ROCECY,
                'deptToEquity': debtToEquity,
                'peGraph': peRatioCS,
                'pbGraph': pbRatioCS,
                'marketCap': round(return_val_or_0(marketCapCS), 2),
                'marketCapBySales': marketCapBySales,
                'evByEbitda': evByEbitda,
            }
        }

        fetchForYear = int(currentYear) - 1
        if latestProfitAndLoss:
            if latestProfitAndLoss.year:
                fetchForYear = latestProfitAndLoss.year
        for company in revenuePeersCompanyList:
            if company.stockStatus == 'Listed' and company.screenerLink:
                screenerDict[company.stockName] = crawlScreenerView(company, fetchForYear=fetchForYear)
            else:
                yearlyData = peerLinkingYearlyData.objects.filter(screenerCompany=company)
                yearlyData_list = []
                if yearlyData:
                    for each in yearlyData:
                        yearlyData_serial = peerLinkingYearlyDataSerializer(each)
                        yearlyData_list.append(yearlyData_serial.data)
                try:
                    stockYearData = yearlyData.get(year=fetchForYear)
                    screenerDict[company.stockName] = {
                        'id': company.pk,
                        'type': company.stockStatus,
                        'fetchedUrl': '',
                        'revenue': stockYearData.revenue,
                        'netProfitMargin': stockYearData.netProfitMargin,
                        'assetTurnoverRation': stockYearData.assetTurnoverRation,
                        'ROE': stockYearData.ROE,
                        'ROCE': stockYearData.ROCE,
                        'deptToEquity': stockYearData.deptToEquity,
                        'peGraph': stockYearData.peRatio,
                        'pbGraph': stockYearData.pbRatio,
                        'marketCap': stockYearData.marketCap,
                        'marketCapBySales': stockYearData.marketCapBySales,
                        'enterpriseVal': stockYearData.enterpriseValue,
                        'evByEbitda': stockYearData.evByEbitda,
                        'cashAndShortTermEquivalents': stockYearData.cashAndShortTermCashEquivalents,
                        'PreferenceEquity': stockYearData.PreferenceEquity,
                        'totalMinorityInterest': stockYearData.totalMinorityInterest,
                        'longTermMarketableSecurities': stockYearData.longTermMarketableSecurities,
                        'yearNotAvailable': '',
                        'yearlyData': yearlyData_list,
                    }
                except:
                    screenerDict[company] = {
                        'id': company.pk,
                        'type': company.stockStatus,
                        'fetchedUrl': '',
                        'revenue': 0,
                        'netProfitMargin': 0,
                        'assetTurnoverRation': 0,
                        'ROE': 0,
                        'ROCE': 0,
                        'deptToEquity': 0,
                        'peGraph': 0,
                        'pbGraph': 0,
                        'marketCap': 0,
                        'marketCapBySales': 0,
                        'enterpriseVal': 0,
                        'evByEbitda': 0,
                        'cashAndShortTermEquivalents': 0,
                        'PreferenceEquity': 0,
                        'totalMinorityInterest': 0,
                        'longTermMarketableSecurities': 0,
                        'yearNotAvailable': '',
                        'yearlyData': yearlyData,
                    }
        stockPeersDescInst_detail = ""
        try:
            stockPeersDescInst = stockPeers.objects.get(stockProfileName=stock)
            if stockPeersDescInst:
                stockPeersDescInst_detail = stockPeersSerializer(stockPeersDescInst)
                stockPeersDescInst_detail = stockPeersDescInst_detail.data
        except:
            stockPeersDescInst = None
        try:
            financialFigureUnitsInst = financialFigureUnits.objects.get(stockProfileName=stock)
        except:
            financialFigureUnitsInst = None
        despositoryOptions, saleType = rightSideMenuObjs_serialized()
        if revenueCY == 0.00 and netProfitMarginCY == 0.00 and \
                totalAssetTurnoverRatioCY == 0.00 and totalFixedAssetTurnoverRatioCY == 0.00 and \
                ROECY == 0.00 and ROCECY == 0.00 and debtToEquity == 0.00 and peRatioCS and \
                pbRatioCS == 0.00 and marketCapCS == 0.00 and marketCapBySales == 0.00 and evByEbitda == 0.00:
            visiblity = False
        else:
            visiblity = True

        response_dict = {}
        keys = ['marketCapDescription', 'revenueDescription', 'pbDescription', 'peDescription',
                'netProfitMarginDescription', 'evByEbitdaDescription', 'marketCapBySalesDescription',
                'assestTurnOverRatioDescription', 'fixedAssetTurnoverRatioDescription', 'ROEDescription',
                'ROCEDescription', 'DebtToEquityDescription']
        for item in keys:
            del stockPeersDescInst_detail[item]
        stock_detail = {}
        # stock_detail['screenerDict'] = screenerDict
        stock_detail['extraData'] = stockPeersDescInst_detail
        stock_detail['extraData']['stockName'] = stock.stockName
        stock_detail['extraData']['seoTitle'] = stock.seoTitle
        stock_detail['extraData']['graphVisiblity'] = visiblity

        stock_detail['data'] = []
        marketCap_list = []
        revenue_list = []
        netProfit_list = []  # currently not found
        netProfitMargin_list = []
        netInterestIncome_list = []  # currently not found
        priceByBookValue_list = []  # currently not found
        priceByEarning_list = []  # currently not found
        totalAssetUnderManagement = []  # currently not found
        roa_dict = []  # currently not found
        roe_list = []
        debtToEquity_list = []
        assetTurnoverRation_list = []
        evByEbitda_list = []
        marketCapBySales_list = []
        peGraph_list = []
        pbGraph_list = []
        roce_list = []

        if screenerDict:
            for company in screenerDict:
                # if type(company) != str:
                #	company = company.stockName

                marketCap_list.append({'name': company, 'value': screenerDict[company]['marketCap']})
                revenue_list.append({'name': company, 'value': screenerDict[company]['revenue']})
                netProfitMargin_list.append({'name': company, 'value': screenerDict[company]['netProfitMargin']})
                roe_list.append({'name': company, 'value': screenerDict[company]['ROE']})
                debtToEquity_list.append({'name': company, 'value': screenerDict[company]['deptToEquity']})
                assetTurnoverRation_list.append(
                    {'name': company, 'value': screenerDict[company]['assetTurnoverRation']})
                evByEbitda_list.append({'name': company, 'value': screenerDict[company]['evByEbitda']})
                marketCapBySales_list.append({'name': company, 'value': screenerDict[company]['marketCapBySales']})
                peGraph_list.append({'name': company, 'value': screenerDict[company]['peGraph']})
                pbGraph_list.append({'name': company, 'value': screenerDict[company]['pbGraph']})
                roce_list.append({'name': company, 'value': screenerDict[company]['ROCE']})

        # if marketCap_list != []:
        #     stock_detail['data'].append(
        #         {'key': 'marketCap', 'label': 'Market Cap', 'description': stockPeersDescInst.marketCapDescription,
        #          'value': marketCap_list})
        # if revenue_list != []:
        #     stock_detail['data'].append(
        #         {'key': 'revenue', 'label': 'Revenue', 'description': stockPeersDescInst.revenueDescription,
        #          'value': revenue_list})
        # if netProfitMargin_list != []:
        #     stock_detail['data'].append({'key': 'netProfitMargin', 'label': 'Net Profit Margin',
        #                                  'description': stockPeersDescInst.netProfitMarginDescription,
        #                                  'value': netProfitMargin_list})
        #
        # if roe_list != []:
        #     stock_detail['data'].append(
        #         {'key': 'roe', 'label': 'ROE', 'description': stockPeersDescInst.ROEDescription, 'value': roe_list})
        # if debtToEquity_list != []:
        #     stock_detail['data'].append({'key': 'debtToEquity', 'label': 'Debt to Equity',
        #                                  'description': stockPeersDescInst.DebtToEquityDescription,
        #                                  'value': debtToEquity_list})
        # if assetTurnoverRation_list != []:
        #     stock_detail['data'].append({'key': 'assetTurnoverRatio', 'label': 'Total Asset Turnover Ratio',
        #                                  'description': stockPeersDescInst.assestTurnOverRatioDescription,
        #                                  'value': assetTurnoverRation_list})
        # if evByEbitda_list != []:
        #     stock_detail['data'].append(
        #         {'key': 'evByEbitda', 'label': 'EV/EBITDA', 'description': stockPeersDescInst.evByEbitdaDescription,
        #          'value': evByEbitda_list})
        # if marketCapBySales_list != []:
        #     stock_detail['data'].append({'key': 'marketCapBySales', 'label': 'Market Cap/Sales',
        #                                  'description': stockPeersDescInst.marketCapBySalesDescription,
        #                                  'value': marketCapBySales_list})
        # if peGraph_list != []:
        #     stock_detail['data'].append(
        #         {'key': 'peGraph', 'label': 'P/E Ratio', 'description': stockPeersDescInst.peDescription,
        #          'value': marketCapBySales_list})
        # if pbGraph_list != []:
        #     stock_detail['data'].append(
        #         {'key': 'pbGraph', 'label': 'P/B Ratio', 'description': stockPeersDescInst.pbDescription,
        #          'value': marketCapBySales_list})
        # if roce_list != []:
        #     stock_detail['data'].append(
        #         {'key': 'roce', 'label': 'ROCE', 'description': stockPeersDescInst.ROCEDescription,
        #          'value': marketCapBySales_list})

        # if stock_detail['_']['data'] == {} and stock_detail['_']['child'] == {}:
        #    stock_detail.pop('_')

        # stock_detail = {'message': company}
        # response_dict.update({'stock': stock_detail})
        """context = {
            'stock': stock_detail,
            'allStockList': allStockList_list,
            'stockPeersDescInst': stockPeersDescInst_detail,
            'stockAdmInst': stockAdmInst_detail,
            'despositoryOptions': despositoryOptions,
            'saleType': saleType,
            'visible': visiblity,
            'screenerDict': screenerDict,
            'year': yearCY,
        }
        return Response({'response': context})"""
        if checkValue(marketCap_list):
            stock_detail['data'].append({'key': 'marketCap', 'label': 'Market Cap', 'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None, 'description': stockPeersDescInst.marketCapDescription, 'value': marketCap_list})
        if checkValue(revenue_list):
            stock_detail['data'].append({'key': 'revenue', 'label': 'Revenue',
                                         'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                         'description': stockPeersDescInst.revenueDescription, 'value': revenue_list})
        if checkValue(pbGraph_list):
            stock_detail['data'].append({'key': 'pbGraph', 'label': 'P/B Ratio', 'value_in': None,
                                         'description': stockPeersDescInst.pbDescription, 'value': pbGraph_list})
        if checkValue(peGraph_list):
            stock_detail['data'].append({'key': 'peGraph', 'label': 'P/E Ratio', 'value_in': None,
                                         'description': stockPeersDescInst.peDescription, 'value': peGraph_list})
        if checkValue(netProfitMargin_list):
            stock_detail['data'].append({'key': 'netProfitMargin', 'label': 'Net Profit Margin', 'value_in': '%',
                                         'description': stockPeersDescInst.netProfitMarginDescription,
                                         'value': netProfitMargin_list})
        if checkValue(evByEbitda_list):
            stock_detail['data'].append({'key': 'evByEbitda', 'label': 'EV/EBITDA', 'value_in': None,
                                         'description': stockPeersDescInst.evByEbitdaDescription,
                                         'value': evByEbitda_list})
        if checkValue(marketCapBySales_list):
            stock_detail['data'].append({'key': 'marketCapBySales', 'label': 'Market Cap/Sales', 'value_in': None,
                                         'description': stockPeersDescInst.marketCapBySalesDescription,
                                         'value': marketCapBySales_list})
        if checkValue(assetTurnoverRation_list):
            stock_detail['data'].append(
                {'key': 'assetTurnoverRatio', 'label': 'Total Asset Turnover Ratio', 'value_in': None,
                 'description': stockPeersDescInst.assestTurnOverRatioDescription, 'value': assetTurnoverRation_list})
        if checkValue(roe_list):
            stock_detail['data'].append(
                {'key': 'roe', 'label': 'ROE', 'value_in': '%', 'description': stockPeersDescInst.ROEDescription,
                 'value': roe_list})
        if checkValue(roce_list):
            stock_detail['data'].append(
                {'key': 'roce', 'label': 'ROCE', 'value_in': '%', 'description': stockPeersDescInst.ROCEDescription,
                 'value': roce_list})
        if checkValue(debtToEquity_list):
            stock_detail['data'].append({'key': 'debtToEquity', 'label': 'Debt to Equity', 'value_in':  None, 'description': stockPeersDescInst.DebtToEquityDescription, 'value': debtToEquity_list})

        return Response({'response': stock_detail})

def checkValue(value):
    nonZero = False
    for obj in value:
        if obj['value'] != 0 and obj['value'] != None:
            nonZero = True
            break
    return nonZero
@api_view(['GET'])
def getPeersForBankNBFCView_02(request, slug):
    stock = get_object_or_404(stockBasicDetail, id=slug)
    stock_detail = ""
    if stock:
        stock_detail = StockSerializer(stock).data
    if stock.status == 'draft' and not request.user.is_staff:
        return redirect('websiteApp:buypreIPOUrl')

    yearCY = totalRevenueCY = netInterestIncomeCY = None
    revenuePeersCompanyList_list = []
    revenuePeersCompanyList = peersCompanyLinkingForBankNBFC.objects.filter(stockProfileName=stock)
    if revenuePeersCompanyList:
        for each in revenuePeersCompanyList:
            revenuePeersCompanyList_list.append(peersCompanyLinkingForBankNBFCSerializer(each).data)
    currentPrice = localOrScreenerPriceView(stock)
    screenerDict = {}
    graphVisiblity = {}
    stockAdmInst_detail = ""
    try:
        stockAdmInst = stockAdmin.objects.get(stockProfileName=stock)
        if stockAdmInst:
            stockAdmInst_detail = stockAdminSerializer(stockAdmInst).data
    except:
        stockAdmInst = None
    try:
        latestProfitAndLoss = stockProfitAndLossBankNBFC.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestProfitAndLoss = None
    try:
        latestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).latest('year')
    except:
        latestBalanceSheet = 0.00
    try:
        secondLatestBalanceSheet = stockBalanceSheetBankNBFC.objects.filter(stockProfileName=stock).order_by('-year')[
                                   1:2]
    except:
        secondLatestBalanceSheet = 0.00
    # latest Profit and Loss
    netInterestIncomeCY = totalRevenueCY = netProfitCY = netInterestIncomeCY = dilutedEPSCY = basicEPSCY = 0
    if latestProfitAndLoss:
        yearCY = latestProfitAndLoss.year
        if latestProfitAndLoss.netInterestIncome:
            netInterestIncomeCY = Decimal(latestProfitAndLoss.netInterestIncome)
            graphVisiblity['netInterestIncomeGraph'] = True
        else:
            graphVisiblity['netInterestIncomeGraph'] = False
        if latestProfitAndLoss.totalRevenue:
            totalRevenueCY = Decimal(latestProfitAndLoss.totalRevenue)
            graphVisiblity['revenueGraph'] = True
        else:
            graphVisiblity['revenueGraph'] = False
        if latestProfitAndLoss.netIncome:
            netProfitCY = Decimal(latestProfitAndLoss.netIncome)
        if latestProfitAndLoss.basicEPS:
            basicEPSCY = Decimal(latestProfitAndLoss.basicEPS)
        if latestProfitAndLoss.dilutedEPS:
            dilutedEPSCY = Decimal(latestProfitAndLoss.dilutedEPS)
    # latest Balance Sheet
    totalAssetCY = totalEquityCY = longTermBorrowingsCY = shortTermBorrowingsCY = 0
    leaseLiabilityCY = currentPortionOfLongTermDebtCY = tangibleBookValueCY = 0
    totalCommonSharesOutstandingCY = tier1CapitalRatioCY = tier2CapitalRatioCY = aumCY = 0
    if latestBalanceSheet:
        if latestBalanceSheet.totalAssets:
            totalAssetCY = latestBalanceSheet.totalAssets
        if latestBalanceSheet.totalEquity:
            totalEquityCY = latestBalanceSheet.totalEquity
        if latestBalanceSheet.longTermBorrowings:
            longTermBorrowingsCY = latestBalanceSheet.longTermBorrowings
        if latestBalanceSheet.shortTermBorrowings:
            shortTermBorrowingsCY = latestBalanceSheet.shortTermBorrowings
        if latestBalanceSheet.leaseLiability:
            leaseLiabilityCY = latestBalanceSheet.leaseLiability
        if latestBalanceSheet.currentPortionOfLongTermDebt:
            currentPortionOfLongTermDebtCY = latestBalanceSheet.currentPortionOfLongTermDebt
        if latestBalanceSheet.tangibleBookValue:
            tangibleBookValueCY = latestBalanceSheet.tangibleBookValue
        if latestBalanceSheet.totalCommonSharesOutstanding:
            totalCommonSharesOutstandingCY = latestBalanceSheet.totalCommonSharesOutstanding
        if latestBalanceSheet.tier1CapitalRatio:
            tier1CapitalRatioCY = latestBalanceSheet.tier1CapitalRatio
            graphVisiblity['tier1Graph'] = True
        else:
            graphVisiblity['tier1Graph'] = False
        if latestBalanceSheet.tier2CapitalRatio:
            tier2CapitalRatioCY = latestBalanceSheet.tier2CapitalRatio
            graphVisiblity['tier2Graph'] = True
        else:
            graphVisiblity['tier2Graph'] = False
        if latestBalanceSheet.aum:
            aumCY = latestBalanceSheet.aum
            graphVisiblity['totalAMUGraph'] = True
        else:
            graphVisiblity['totalAMUGraph'] = False
    # Second latest Balance Sheet
    totalAssetsPY = totalEquityPY = longTermBorrowingsPY = shortTermBorrowingsPY = leaseLiabilityPY = currentPortionOfLongTermDebtPY = 0
    for item in secondLatestBalanceSheet:
        if item:
            if item.totalAssets:
                totalAssetsPY = item.totalAssets
            if item.totalEquity:
                totalEquityPY = item.totalEquity
            if item.longTermBorrowings:
                longTermBorrowingsPY = item.longTermBorrowings
            if item.shortTermBorrowings:
                shortTermBorrowingsPY = item.shortTermBorrowings
            if item.leaseLiability:
                leaseLiabilityPY = item.leaseLiability
            if item.currentPortionOfLongTermDebt:
                currentPortionOfLongTermDebtPY = item.currentPortionOfLongTermDebt
    # Calculating Averages
    avgTotalAsset = avgTotalEquity = avgOfSumNumeratorDE = None
    # if totalAssetCY and totalAssetsPY:
    avgTotalAsset = (return_val_or_0(totalAssetCY) + return_val_or_0(totalAssetsPY)) / 2
    # if totalEquityCY and totalEquityPY:
    avgTotalEquity = (return_val_or_0(totalEquityCY) + return_val_or_0(totalEquityPY)) / 2
    sumForDENumeratorCY = sumForDENumeratorPY = None
    # if longTermBorrowingsCY and shortTermBorrowingsCY and leaseLiabilityCY and currentPortionOfLongTermDebtCY:
    sumForDENumeratorCY = return_val_or_0(longTermBorrowingsCY) + return_val_or_0(
        shortTermBorrowingsCY) + return_val_or_0(leaseLiabilityCY) + return_val_or_0(currentPortionOfLongTermDebtCY)
    # if longTermBorrowingsPY and shortTermBorrowingsPY and leaseLiabilityPY and currentPortionOfLongTermDebtPY:
    sumForDENumeratorPY = return_val_or_0(longTermBorrowingsPY) + return_val_or_0(
        shortTermBorrowingsPY) + return_val_or_0(leaseLiabilityPY) + return_val_or_0(currentPortionOfLongTermDebtPY)
    # if sumForDENumeratorCY and sumForDENumeratorPY:
    avgOfSumNumeratorDE = (sumForDENumeratorCY + sumForDENumeratorPY) / 2
    # formulas and calculations
    # if netProfitCY and avgTotalAsset:
    roa = return_val_or_0(netProfitCY) / return_val_or_1(avgTotalAsset)
    if roa and roa != 0:
        graphVisiblity['roaGraph'] = True
    else:
        graphVisiblity['roaGraph'] = False
    # else:
    # 	roa = 0
    # if netProfitCY and netInterestIncomeCY:
    netProfitMarginPercentage = (return_val_or_0(netProfitCY) / return_val_or_1(netInterestIncomeCY)) * 100
    if netProfitMarginPercentage and netProfitMarginPercentage != 0:
        graphVisiblity['netProfitMarginPercentageGraph'] = True
    else:
        graphVisiblity['netProfitMarginPercentageGraph'] = False
    # else:
    # 	netProfitMarginPercentage = 0
    # if netInterestIncomeCY and avgTotalAsset:
    assetTurnOverRatio = return_val_or_0(netInterestIncomeCY) / return_val_or_1(avgTotalAsset)
    if assetTurnOverRatio and assetTurnOverRatio != 0:
        graphVisiblity['assetTurnOverRatioGraph'] = True
    else:
        graphVisiblity['assetTurnOverRatioGraph'] = False
    # else:
    # 	assetTurnOverRatio = 0
    # if netProfitCY and avgTotalEquity:
    roeGraph = False
    roe = return_val_or_0(netProfitCY) / return_val_or_1(avgTotalEquity)
    if roe and roe != 0:
        graphVisiblity['roeGraph'] = True
    else:
        graphVisiblity['roeGraph'] = False
    # else:
    # roe = 0
    # eps = check_eps_basic_or_diluted(basicEPSCY, dilutedEPSCY)
    # if currentPrice and eps:
    # 	priceToEarning = currentPrice / eps
    # else:
    # 	priceToEarning = 0
    priceToEarning, priceToBookVal = currentStockPEPBBankNBFCView(stock)
    if priceToEarning and priceToEarning != 0:
        graphVisiblity['priceToEarningGraph'] = True
    else:
        graphVisiblity['priceToEarningGraph'] = False
    if priceToBookVal and priceToBookVal != 0:
        graphVisiblity['priceToBookValGraph'] = True
    else:
        graphVisiblity['priceToBookValGraph'] = False

    # try:
    # 	bookValueObj = bookValueData.objects.get(stockProfileName=stock,year=yearCY)
    # 	bookValueCY = bookValueObj.bookValue
    # except:
    # 	bookValueCY = 0
    # if currentPrice and bookValueCY:
    # 	if bookValueCY == 0:
    # 		bookValueCY = 1
    # 	priceToBookVal = currentPrice / bookValueCY
    # else:
    # 	priceToBookVal = 0
    # if netInterestIncomeCY and avgTotalAsset:
    nim = return_val_or_0(netInterestIncomeCY) / return_val_or_1(avgTotalAsset)
    if nim and nim != 0:
        graphVisiblity['nimGraph'] = True
    else:
        graphVisiblity['nimGraph'] = False
    # else:
    # 	nim = 0
    # if avgTotalEquity and avgOfSumNumeratorDE:
    debtToEquityRatioGraph = False
    debtToEquityRatio = return_val_or_0(avgOfSumNumeratorDE) / return_val_or_1(avgTotalEquity)
    if debtToEquityRatio and debtToEquityRatio != 0:
        graphVisiblity['debtToEquityRatioGraph'] = True
    else:
        graphVisiblity['debtToEquityRatioGraph'] = False
    # else:
    # 	debtToEquityRatio = 0

    # Coming from Key Ratios
    try:
        rorwaGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock,
                                                                    graphFor='Return on Risk Weighted Assets(RORWA)')
        rorwaInstCY = industrySpecificGraphsValues.objects.get(valuesFor=rorwaGraphFromKeyRatio, year=yearCY)
        RORWAVal = rorwaInstCY.value
        graphVisiblity['RORWAGraph'] = True
    except:
        RORWAVal = 0
        graphVisiblity['RORWAGraph'] = False
    try:
        netNPAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='Net NPA')
        netNPAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=netNPAGraphFromKeyRatio, year=yearCY)
        netNPAVal = netNPAInstCY.value
        graphVisiblity['netNPAGraph'] = True
    except:
        netNPAVal = 0
        graphVisiblity['netNPAGraph'] = False
    try:
        CASAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='CASA')
        CASAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=CASAGraphFromKeyRatio, year=yearCY)
        CASAVal = CASAInstCY.value
        graphVisiblity['casaGraph'] = True
    except:
        CASAVal = 0
        graphVisiblity['casaGraph'] = False
    try:
        grossNPAGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock, graphFor='Gross NPA')
        grossNPAInstCY = industrySpecificGraphsValues.objects.get(valuesFor=grossNPAGraphFromKeyRatio, year=yearCY)
        grossNPAVal = grossNPAInstCY.value
        graphVisiblity['grossNPAValGraph'] = True
    except:
        grossNPAVal = 0
        graphVisiblity['grossNPAValGraph'] = False
    try:
        CARGraphFromKeyRatio = industrySpecificGraphs.objects.get(stockProfileName=stock,
                                                                  graphFor='Capital Adequacy Ratio(CAR)')
        CARInstCY = industrySpecificGraphsValues.objects.get(valuesFor=CARGraphFromKeyRatio, year=yearCY)
        carVal = CARInstCY.value
        graphVisiblity['carGraph'] = True
    except:
        carVal = 0
        graphVisiblity['carGraph'] = False
    # P/TB Calculation
    # if currentPrice and tangibleBookValueCY and totalCommonSharesOutstandingCY:
    # 	if totalCommonSharesOutstandingCY == 0:
    # 		totalCommonSharesOutstandingCY = 1
    pByTB = return_val_or_0(currentPrice) / return_val_or_1(
        (return_val_or_0(tangibleBookValueCY) * 10000000) / return_val_or_1(totalCommonSharesOutstandingCY))
    if pByTB and pByTB != 0:
        graphVisiblity['pByTBGraph'] = True
    else:
        graphVisiblity['pByTBGraph'] = False
    # else:
    # 	pByTB = 0
    marketCapCS = marketCapView(stock)
    try:
        if stock.stockProfileNameFFU.financialNumbers == 'L':
            marketCapCS = numberConversion(marketCapCS, currentSystem='Cr',
                                           convertTo=stock.stockProfileNameFFU.financialNumbers)
    except:
        pass
    # print('---------------------------------------------------------------------Jhalak new TESTSTING STARTSSSSSSSS---------------------------------------------------------------------')
    # print(marketCapCS)
    # print('---------------------------------------------------------------------Jhalak new TESTSTING ENDDDDDDDSSSS---------------------------------------------------------------------')
    stockname = str(stock_detail.get("stockName"))
    screenerDict[stockname] = {
        'id': stock.id,
        'type': 'current',
        'revenue': round(return_val_or_0(totalRevenueCY), 2),
        'netInterestIncome': round(return_val_or_0(netInterestIncomeCY), 2),

        'marketCap': round(return_val_or_0(marketCapCS), 2),

        'roa': round((roa * 100), 2),
        'netProfitMarginPercentage': round(netProfitMarginPercentage, 2),
        'assetTurnOverRatio': round(assetTurnOverRatio, 2),
        'roe': round((roe * 100), 2),
        'car': round(carVal, 2),
        'netNPA': round(netNPAVal, 2),
        'grossNPA': round(grossNPAVal, 2),
        'stockPE': round(priceToEarning, 2),
        'stockPB': round(priceToBookVal, 2),
        'nim': round((nim * 100), 2),
        'CASA': round(CASAVal, 2),
        'debtToEquityRatio': round(debtToEquityRatio, 2),
        'pByTB': round(pByTB, 2),
        'tier1': round(tier1CapitalRatioCY, 2),
        'tier2': round(tier2CapitalRatioCY, 2),
        'totalAMU': round(aumCY, 2),
        'RORWA': round(RORWAVal, 2),
    }
    fetchForYear = int(currentYear) - 1
    if latestProfitAndLoss:
        if latestProfitAndLoss.year:
            fetchForYear = latestProfitAndLoss.year
    for company in revenuePeersCompanyList:
        if company.stockStatus == 'Listed' and company.screenerLink:
            someVal = crawlScreenerForBankNBFCView(company, fetchForYear=fetchForYear)
            yearlyData_list = []
            if someVal['yearlyData']:
                for each in someVal['yearlyData']:
                    yearlyData_list.append(peerLinkingYearlyDataForBankNBFCSerializer(each).data)
            someVal['yearlyData'] = yearlyData_list
            screenerDict[company.stockName] = someVal
        else:
            unlistedYearlyData_list = []
            unlistedYearlyData = peerLinkingYearlyDataForBankNBFC.objects.filter(screenerCompany=company)
            if unlistedYearlyData:
                unlistedYearlyData_list.append(peerLinkingYearlyDataForBankNBFCSerializer(each).data)

            try:
                companyYearlyInst = unlistedYearlyData.get(year=fetchForYear)
                manualCAR = companyYearlyInst.CAR
                manualMarketCap = companyYearlyInst.marketCap
                manualnetNPA = companyYearlyInst.netNPA
                manualgrossNPA = companyYearlyInst.grossNPA
                manualCASA = companyYearlyInst.CASA
                manualtier1CapitalRatio = companyYearlyInst.tier1CapitalRatio
                manualtier2CapitalRatio = companyYearlyInst.tier2CapitalRatio
                manualtotalAMU = companyYearlyInst.totalAMU
                manualRORWA = companyYearlyInst.RORWA
                manualnumberOfShares = companyYearlyInst.numberOfShares
                manualintangibleAssests = companyYearlyInst.intangibleAssests
                manualnetInterestIncome = companyYearlyInst.netInterestIncome
                manualrevenue = companyYearlyInst.revenue
                manualroa = companyYearlyInst.roa
                manualnetProfitMargin = companyYearlyInst.netProfitMargin
                manualassetTurnOverRatio = companyYearlyInst.assetTurnOverRatio
                manualROE = companyYearlyInst.ROE
                manualpeRatio = companyYearlyInst.peRatio
                manualpbRatio = companyYearlyInst.pbRatio
                manualNIM = companyYearlyInst.NIM
                manualDERatio = companyYearlyInst.DERatio
                manualpriceByTangibleBookRatio = companyYearlyInst.priceByTangibleBookRatio
                if company.screenerLink:
                    manualScreenerLink = company.screenerLink
                else:
                    manualScreenerLink = None
            except:
                manualCAR = 0
                manualMarketCap = 0
                manualnetNPA = 0
                manualgrossNPA = 0
                manualCASA = 0
                manualtier1CapitalRatio = 0
                manualtier2CapitalRatio = 0
                manualtotalAMU = 0
                manualRORWA = 0
                manualnumberOfShares = 0
                manualintangibleAssests = 0
                manualnetInterestIncome = 0
                manualrevenue = 0
                manualroa = 0
                manualnetProfitMargin = 0
                manualassetTurnOverRatio = 0
                manualROE = 0
                manualpeRatio = 0
                manualpbRatio = 0
                manualNIM = 0
                manualDERatio = 0
                manualpriceByTangibleBookRatio = 0
                manualScreenerLink = None
            screenerDict[company.stockName] = {
                'id': company.id,
                'type': 'Unlisted',
                'car': manualCAR,
                'marketCap': manualMarketCap,
                'netNPA': manualnetNPA,
                'grossNPA': manualgrossNPA,
                'CASA': manualCASA,
                'tier1': manualtier1CapitalRatio,
                'tier2': manualtier2CapitalRatio,
                'totalAMU': manualtotalAMU,
                'RORWA': manualRORWA,
                'numberOfShares': manualnumberOfShares,
                'intangibleAssests': manualintangibleAssests,
                'netInterestIncome': manualnetInterestIncome,
                'revenue': manualrevenue,
                'roa': manualroa,
                'netProfitMarginPercentage': manualnetProfitMargin,
                'assetTurnOverRatio': manualassetTurnOverRatio,
                'roe': manualROE,
                'stockPE': manualpeRatio,
                'stockPB': manualpbRatio,
                'nim': manualNIM,
                'debtToEquityRatio': manualDERatio,
                'pByTB': manualpriceByTangibleBookRatio,
                'fetchedUrl': manualScreenerLink,
                'yearlyData': unlistedYearlyData_list,
            }

    # if latestProfitAndLoss:
    # 	if latestProfitAndLoss.year:
    # 		fetchForYear = latestProfitAndLoss.year
    # 	else:
    # 		fetchForYear = 2021
    # for company in revenuePeersCompanyList:
    # 	if company.screenerLink:
    # 		dictForScreenerData = crawlScreenerForBankNBFCView(company, fetchForYear= fetchForYear)
    # 		return HttpResponse(str(dictForScreenerData))
    # 		screenerDict[company] = dictForScreenerData
    stockPeersDescInst_detail = ""
    try:
        stockPeersDescInst = stockPeers.objects.get(stockProfileName=stock)
        if stockPeersDescInst:
            stockPeersDescInst_detail = stockPeersSerializer(stockPeersDescInst).data
    except:
        stockPeersDescInst = None
    peersCompanyDesc = stockPeersForm(instance=stockPeersDescInst)
    peersCompanyLinkingCreate = peersCompanyLinkingForBankNBFCForm()
    # despositoryOptions, saleType = rightSideMenuObjs()
    createpeerLinkingYearlyDataForm = peerLinkingYearlyDataForBankNBFCForm()
    stockPeersDescriptionForBankNBFCInst_detail = ""
    try:
        stockPeersDescriptionForBankNBFCInst = stockPeersDescriptionForBankNBFC.objects.get(stockProfileName=stock)
        if stockPeersDescriptionForBankNBFCInst:
            stockPeersDescriptionForBankNBFCInst_detail = stockPeersDescriptionForBankNBFCSerializer(
                stockPeersDescriptionForBankNBFCInst).data
    except:
        stockPeersDescriptionForBankNBFCInst = None
    stockPeersDescriptionForBankNBFCInstForm = stockPeersDescriptionForBankNBFCForm(
        instance=stockPeersDescriptionForBankNBFCInst)

    if totalRevenueCY == 0.00 and netInterestIncomeCY == 0.00 and \
            marketCapCS == 0.00 and netProfitMarginPercentage == 0.00 and \
            assetTurnOverRatio == 0.00 and roa == 0.00 and roe == 0.00 and carVal and \
            netNPAVal == 0.00 and grossNPAVal == 0.00 and priceToEarning == 0.00 and priceToBookVal == 0.00 and \
            nim == 0.00 and CASAVal == 0.00 and debtToEquityRatio == 0.00 and pByTB == 0.00 and \
            tier1CapitalRatioCY == 0.00 and aumCY == 0.00 and RORWAVal == 0.00:
        visiblity = False
    else:
        visiblity = True

    screenerDict_new = {}
    i = 0
    for company in screenerDict:
        i += 1
        if type(company) != stockBasicDetail:
            screenerDict_new[company] = screenerDict[company]

    response_dict = {}
    keys = ['marketCapDescription', 'revenueDescription', 'pbDescription', 'peDescription',
            'netProfitMarginDescription', 'evByEbitdaDescription', 'marketCapBySalesDescription',
            'assestTurnOverRatioDescription', 'fixedAssetTurnoverRatioDescription', 'ROEDescription', 'ROCEDescription',
            'DebtToEquityDescription']
    for item in keys:
        del stockPeersDescInst_detail[item]

    stock_detail = {}
    # stock_detail['screenerdict'] = screenerDict
    stock_detail['extraData'] = stockPeersDescInst_detail
    stock_detail['extraData']['stockName'] = stock.stockName
    stock_detail['extraData']['seoTitle'] = stock.seoTitle
    stock_detail['extraData']['graphVisiblity'] = graphVisiblity

    # stock_detail['_'] = {'data': {}, 'child': {}}
    stock_detail['data'] = []
    marketCap_list = []
    revenue_list = []
    # netProfit_dict = {} # currently not found
    netInterestIncome_list = []
    CASA_list = []
    grossNPA_list = []
    netNPA_list = []
    netInterestMargin_list = []
    netProfitMargin_list = []
    # netInterestIncome_dict = {} # currently not found
    # priceByBookValue_dict = {} # currently not found
    priceByEarning_list = []  # currently not found
    totalAssetUnderManagement_list = []
    roa_list = []
    roe_list = []
    car_list = []
    debtToEquity_list = []
    pByTB_list = []
    tier1CapitalRatio_list = []
    assetTurnoverRatio_list = []
    RORWA_list = []
    tier2CapitalRatio_list = []
    stockPE_list = []
    stockPB_list = []
    # evByEbitda_dict = {}
    # marketCapBySales_dict = {}
    if screenerDict:
        for company in screenerDict:
            # if type(company) != str:
            #	company = company.stockName

            marketCap_list.append({'name': company, 'value': screenerDict[company]['marketCap']})
            revenue_list.append({'name': company, 'value': screenerDict[company]['revenue']})
            netInterestIncome_list.append({'name': company, 'value': screenerDict[company]['netInterestIncome']})
            totalAssetUnderManagement_list.append({'name': company, 'value': screenerDict[company]['totalAMU']})
            CASA_list.append({'name': company, 'value': screenerDict[company]['CASA']})
            grossNPA_list.append({'name': company, 'value': screenerDict[company]['grossNPA']})
            netNPA_list.append({'name': company, 'value': screenerDict[company]['netNPA']})
            netInterestMargin_list.append({'name': company, 'value': screenerDict[company]['nim']})
            netProfitMargin_list.append({'name': company, 'value': screenerDict[company]['netProfitMarginPercentage']})
            roa_list.append({'name': company, 'value': screenerDict[company]['roa']})
            roe_list.append({'name': company, 'value': screenerDict[company]['roe']})
            car_list.append({'name': company, 'value': screenerDict[company]['car']})
            debtToEquity_list.append({'name': company, 'value': screenerDict[company]['debtToEquityRatio']})
            pByTB_list.append({'name': company, 'value': screenerDict[company]['pByTB']})
            tier1CapitalRatio_list.append({'name': company, 'value': screenerDict[company]['tier1']})
            assetTurnoverRatio_list.append({'name': company, 'value': screenerDict[company]['assetTurnOverRatio']})
            RORWA_list.append({'name': company, 'value': screenerDict[company]['RORWA']})
            tier2CapitalRatio_list.append({'name': company, 'value': screenerDict[company]['tier2']})
            stockPE_list.append({'name': company, 'value': screenerDict[company]['stockPE']})
            stockPB_list.append({'name': company, 'value': screenerDict[company]['stockPB']})
            # evByEbitda_dict[company] = screenerDict[company]['evByEbitda']
            # marketCapBySales_dict[company] = screenerDict[company]['marketCapBySales']

    # if marketCap_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'marketCap', 'label': 'Market Cap', 'description': stockPeersDescInst.marketCapDescription,
    #          'value': marketCap_list})
    # if revenue_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'revenue', 'label': 'Revenue', 'description': stockPeersDescInst.revenueDescription,
    #          'value': revenue_list})
    # if netInterestIncome_list != []:
    #     stock_detail['data'].append({'key': 'netInterestIncome', 'label': 'Net Interest Income', 'description': None,
    #                                  'value': netInterestIncome_list})
    # if totalAssetUnderManagement_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'totalAssetUnderManagement', 'label': 'Total Asset under Management', 'description': None,
    #          'value': totalAssetUnderManagement_list})
    # if stockPE_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'stockPE', 'label': 'Price/Earning', 'description': None, 'value': stockPE_list})
    # if stockPB_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'stockPB', 'label': 'Price/Book Value', 'description': None, 'value': stockPB_list})
    # if CASA_list != []:
    #     stock_detail['data'].append({'key': 'CASA', 'label': 'CASA', 'description': None, 'value': CASA_list})
    # if grossNPA_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'grossNPA', 'label': 'Gross NPA', 'description': None, 'value': grossNPA_list})
    # if netNPA_list != []:
    #     stock_detail['data'].append({'key': 'netNPA', 'label': 'Net NPA', 'description': None, 'value': netNPA_list})
    # if netInterestMargin_list != []:
    #     stock_detail['data'].append({'key': 'netInterestMargin', 'label': 'Net Interest Margin', 'description': None,
    #                                  'value': netInterestMargin_list})
    # if netProfitMargin_list != []:
    #     stock_detail['data'].append({'key': 'netProfitMargin', 'label': 'Net Profit Margin',
    #                                  'description': stockPeersDescInst.netProfitMarginDescription,
    #                                  'value': netProfitMargin_list})
    # if roa_list != []:
    #     stock_detail['data'].append({'key': 'roa', 'label': 'ROA', 'description': None, 'value': roa_list})
    # if roe_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'roe', 'label': 'ROE', 'description': stockPeersDescInst.ROEDescription, 'value': roe_list})
    # if car_list != []:
    #     stock_detail['data'].append({'key': 'car', 'label': 'CAR', 'description': None, 'value': car_list})
    # if debtToEquity_list != []:
    #     stock_detail['data'].append({'key': 'debtToEquity', 'label': 'Debt to Equity Ratio',
    #                                  'description': stockPeersDescInst.DebtToEquityDescription,
    #                                  'value': debtToEquity_list})
    # if pByTB_list != []:
    #     stock_detail['data'].append(
    #         {'key': 'pByTB', 'label': 'Price by Tangible Book Value', 'description': None, 'value': pByTB_list})
    # if tier1CapitalRatio_list != []:
    #     stock_detail['data'].append({'key': 'tier1CapitalRatio', 'label': 'Tier 1 Capital Ratio', 'description': None,
    #                                  'value': tier1CapitalRatio_list})
    # if assetTurnoverRatio_list != []:
    #     stock_detail['data'].append({'key': 'assetTurnoverRatio', 'label': 'Asset Turnover Ratio',
    #                                  'description': stockPeersDescInst.assestTurnOverRatioDescription,
    #                                  'value': assetTurnoverRatio_list})
    # if RORWA_list != []:
    #     stock_detail['data'].append({'key': 'RORWA', 'label': 'RORWA', 'description': None, 'value': RORWA_list})
    # if tier2CapitalRatio_list != []:
    #     stock_detail['data'].append({'key': 'tier2CapitalRatio', 'label': 'Tier 2 Capital Ratio', 'description': None,
    #                                  'value': tier2CapitalRatio_list})

    # response_dict.update({'stock': stock_detail})

    '''context = {
        'stock': stock_detail,
        #'peersCompanyDesc':peersCompanyDesc,
        'stockPeersDescInst':stockPeersDescInst_detail,
        'stockAdmInst':stockAdmInst_detail,
        #'peersCompanyLinkingCreate':peersCompanyLinkingCreate,
        'screenerDict': screenerDict,
        'year': yearCY,
        #'createpeerLinkingYearlyDataForm': createpeerLinkingYearlyDataForm,
        'stockPeersDescriptionForBankNBFCInst':stockPeersDescriptionForBankNBFCInst_detail,
        #'stockPeersDescriptionForBankNBFCInstForm':stockPeersDescriptionForBankNBFCInstForm,
        'graphVisiblity': graphVisiblity,
        'visible':visiblity,
    }'''
    if checkValue(marketCap_list):
        stock_detail['data'].append({'key': 'marketCap', 'label': 'Market Cap',
                                     'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                     'description': stockPeersDescInst.marketCapDescription,
                                     'value': marketCap_list})
    if checkValue(revenue_list):
        stock_detail['data'].append({'key': 'revenue', 'label': 'Revenue',
                                     'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                     'description': stockPeersDescInst.revenueDescription,
                                     'value': revenue_list})
    if checkValue(netInterestIncome_list):
        stock_detail['data'].append({'key': 'netInterestIncome', 'label': 'Net Interest Income',
                                     'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                     'description': stockPeersDescriptionForBankNBFCInst.netInterestIncomeDescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': netInterestIncome_list})
    if checkValue(totalAssetUnderManagement_list):
        stock_detail['data'].append({'key': 'totalAssetUnderManagement', 'label': 'Total Asset under Management',
                                     'value_in': financialFigureUnitsInst.financialNumbers if financialFigureUnitsInst else None,
                                     'description': stockPeersDescriptionForBankNBFCInst.totalAMUDescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': totalAssetUnderManagement_list})
    if checkValue(stockPB_list):
        stock_detail['data'].append({'key': 'stockPB', 'label': 'Price/Book Value', 'value_in': None,
                                     'description': stockPeersDescriptionForBankNBFCInst.PBDescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': stockPB_list})
    if checkValue(stockPE_list):
        stock_detail['data'].append({'key': 'stockPE', 'label': 'Price/Earning', 'value_in': None,
                                     'description': stockPeersDescriptionForBankNBFCInst.PEDescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': stockPE_list})
    if checkValue(CASA_list):
        stock_detail['data'].append({'key': 'CASA', 'label': 'CASA', 'value_in': None,
                                     'description': stockPeersDescriptionForBankNBFCInst.CASADescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': CASA_list})
    if checkValue(grossNPA_list):
        stock_detail['data'].append({'key': 'grossNPA', 'label': 'Gross NPA', 'value_in': '%',
                                     'description': stockPeersDescriptionForBankNBFCInst.grossNPADescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': grossNPA_list})
    if checkValue(netNPA_list):
        stock_detail['data'].append({'key': 'netNPA', 'label': 'Net NPA', 'value_in': '%',
                                     'description': stockPeersDescriptionForBankNBFCInst.netNPADescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': netNPA_list})
    if checkValue(netInterestMargin_list):
        stock_detail['data'].append({'key': 'netInterestMargin', 'value_in': '%', 'label': 'Net Interest Margin',
                                     'description': stockPeersDescriptionForBankNBFCInst.nimDescription if stockPeersDescriptionForBankNBFCInst else None,
                                     'value': netInterestMargin_list})
    if checkValue(netProfitMargin_list):
        stock_detail['data'].append({'key': 'netProfitMargin', 'value_in': '%', 'label': 'Net Profit Margin', 'description': stockPeersDescriptionForBankNBFCInst.netProfitMarginDescription if stockPeersDescriptionForBankNBFCInst else None, 'value': netProfitMargin_list})
    if checkValue(roa_list):
        stock_detail['data'].append({'key': 'roa', 'label': 'ROA', 'value_in': '%', 'description': stockPeersDescriptionForBankNBFCInst.roaDescription if stockPeersDescriptionForBankNBFCInst else None, 'value': roa_list})
    if checkValue(roe_list):
        stock_detail['data'].append({'key': 'roe', 'label': 'ROE', 'value_in': '%', 'description': stockPeersDescriptionForBankNBFCInst.roeDescription if stockPeersDescriptionForBankNBFCInst else None, 'value': roe_list})
    if checkValue(car_list):
        stock_detail['data'].append({'key': 'car', 'label': 'CAR', 'value_in': '%', 'description': stockPeersDescriptionForBankNBFCInst.carDescriptionDescription if stockPeersDescriptionForBankNBFCInst else None, 'value': car_list})
    if checkValue(debtToEquity_list):
        stock_detail['data'].append({'key': 'debtToEquity', 'label': 'Debt to Equity Ratio', 'value_in': None, 'description': stockPeersDescriptionForBankNBFCInst.debtToEquityRatioDescription if stockPeersDescriptionForBankNBFCInst else None, 'value': debtToEquity_list})
    if checkValue(pByTB_list):
        stock_detail['data'].append({'key': 'pByTB', 'label': 'Price by Tangible Book Value', 'value_in': None, 'description': stockPeersDescriptionForBankNBFCInst.pByTBDescription if stockPeersDescriptionForBankNBFCInst else None, 'value': pByTB_list})
    if checkValue(tier1CapitalRatio_list):
        stock_detail['data'].append({'key': 'tier1CapitalRatio', 'label': 'Tier 1 Capital Ratio', 'value_in': '%', 'description': stockPeersDescriptionForBankNBFCInst.tier1Description if stockPeersDescriptionForBankNBFCInst else None, 'value': tier1CapitalRatio_list})
    if checkValue(assetTurnoverRatio_list):
        stock_detail['data'].append({'key': 'assetTurnoverRatio', 'label': 'Asset Turnover Ratio', 'value_in': None, 'description': stockPeersDescriptionForBankNBFCInst.assetTurnOverRatioDescription if stockPeersDescriptionForBankNBFCInst else None, 'value': assetTurnoverRatio_list})
    print(checkValue(RORWA_list))
    if checkValue(RORWA_list):
        stock_detail['data'].append({'key': 'RORWA', 'label': 'RORWA', 'value_in': None, 'description': stockPeersDescriptionForBankNBFCInst.RORWADescription if stockPeersDescriptionForBankNBFCInst else None, 'value': RORWA_list})
    if checkValue(tier2CapitalRatio_list):
        stock_detail['data'].append({'key': 'tier2CapitalRatio', 'label': 'Tier 2 Capital Ratio', 'value_in': '%', 'description': stockPeersDescriptionForBankNBFCInst.tier2Description if stockPeersDescriptionForBankNBFCInst else None, 'value': tier2CapitalRatio_list})

    return Response({'response': stock_detail})
    # return render(request, 'UI/peersForBankNBFC.html', context)



def financial_mapping():
	
	HIDDEN = "hidden"
	UN_HIDDEN = "not hidden"
	
	normal_mapping = [{'label': 'Total Revenue',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'totalRevenue'},
 {'label': 'COGS',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'costOfGoodsSold'},
 {'label': 'Gross Profit',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'grossProfit'},
 {'label': 'Raw Materials',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'rawMaterials'},
 {'label': 'Power & Fuel Cost',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'powerAndFuelCost'},
 {'label': 'Employee Cost',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'employeeCost'},
 {'label': 'Sales & Administrative Expenses',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'sellingAndAdministrativeExpenses'},
 {'label': 'Operating & Other Expenses',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'operatingAndOtherExpenses'},
 {'label': 'EBITDA',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'ebidta'},
 {'label': 'Depreciation/ Amortization',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'depreciationAndAmortization'},
 {'label': 'PBIT',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'pbit'},
 {'label': 'Interest & Income',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'interestIncome'},
 {'label': 'Interest & Expense',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'interestExpense'},
 {'label': 'Other Items',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'otherItems'},
 {'label': 'PBT',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'pbt'},
 {'label': 'Taxes & Other Items',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'taxesAndOtherItems'},
 {'label': 'Net Income',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'netIncome'},
 {'label': 'Diluted EPS',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'dilutedEPS'},
 {'label': 'Basic EPS',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'basicEPS'},
 {'label': 'DPS',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'DPS'},
 {'label': 'Payout Ratio',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'payoutRatio'},
 {'label': 'Cash & Short Term Investments',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'cashAndShortTermInvestments'},
 {'label': 'Total Receivables',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'totalReceivables'},
 {'label': 'Total Inventory',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'totalInventory'},
 {'label': 'Prepaid Expenses',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'prepaidExpenses'},
 {'label': 'Current Investments',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'currentInvestments'},
 {'label': 'Other Current Financial Assets',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherCurrentFinancialAssets'},
 {'label': 'Loan & Advances',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'loanAndAdvances'},
 {'label': 'Deferred Tax Assest',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'deferredTaxAssest'},
 {'label': 'Current Assets',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': '+',
  'key': 'currentAssets'},
 {'label': 'Net Property/Plant/Equipment',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'netPropertyORPlantOREquipment'},
 {'label': 'Goodwill',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'goodWill'},
 {'label': 'Other Intangible Assets',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherIntangibleAssests'},
 {'label': 'Intangible Assets Under Development',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'intangibleAssestsUnderDevelopment'},
 {'label': 'Long Term Investments',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'longTermInvestments'},
 {'label': 'Deferred Tax Assets (Net)',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'deferredTaxAssetsNet'},
 {'label': 'Other Non Current Assets',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'otherNonCurrentAssets'},
 {'label': 'Non Current Assets',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': '=',
  'key': 'nonCurrentAssets'},
 {'label': 'Total Assets',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalAssets'},
 {'label': 'Accounts Payable',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'accountPayable'},
 {'label': 'Total Deposits',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'totalDeposits'},
 {'label': 'Current Portion of Long Term Debt',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'currentPortionOfLongTermDebt'},
 {'label': 'Unearned Revenue',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'unearnedRevenue'},
 {'label': 'Current Portion of Leases',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'currentPortionOfLeases'},
 {'label': 'Other Current Liabilities',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'otherCurrentLiabilities'},
 {'label': 'Current Liabilities',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': '+',
  'key': 'currentLiabilities'},
 {'label': 'Total Long Term Debt',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'totalLongTermDebt'},
 {'label': 'Long Term Portion of Leases',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'longTermPortionOfLeases'},
 {'label': 'Deferred Tax Liabilities (Net)',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'deferredTaxLiabilities'},
 {'label': 'Other Non Current Liabilities',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'otherNonCurrentLiabilities'},
 {'label': 'Non Current Liablities',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': '=',
  'key': 'nonCurrentLiabilities'},
 {'label': 'Total Liabilities',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': '+',
  'key': 'totalLiabilities'},
 {'label': 'Common Stock',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'commonStock'},
 {'label': 'Other Equity',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherEquity'},
 {'label': 'Reserves & Surplus',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'reservesAndSurplus'},
 {'label': 'Additional Paid-in Capital',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'additionalPaidInCapital'},
 {'label': 'Retained Earnings',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'retainedEarnings'},
 {'label': 'Minority Interest',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'minorityInterest'},
 {'label': 'Treasure Stock',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'treasureStock'},
 {'label': 'Comprehensive Inc. & Other',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'comprehensiveIncAndOther'},
 {'label': 'Total Equity',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': '=',
  'key': 'totalEquity'},
 {'label': 'Total Common Shares Outstanding',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalCommonSharesOutstanding'},
 {'label': "Total Liabilities & Shareholder's Equity",
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalLiabilitiesShareHolderHistory'},
 {'label': 'Cash from Operating Activities',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'cashFromOperatingActivities'},
 {'label': 'Cash from Investing Activities',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'cashFromInvestingActivities'},
 {'label': 'Cash from Financing Activities',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'cashFromFinancingActivities'},
 {'label': 'Net Change in Cash',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'netChangeInCash'},
 {'label': 'Change in Working Capital',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'changesInWorkingCapital'},
 {'label': 'Capital Expenditures',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'capitalExpenditures'},
 {'label': 'Free Cash Flow',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'freeCashFlow'}]

	nbfc_mapping = [{'label': 'Total Revenue',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'totalRevenue'},
 {'label': 'COGS - Repairs and maintainance',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'cogsMinusRepairsMaintenance'},
 {'label': 'Gross Profit',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'grossProfit'},
 {'label': 'Salaries and Other Empl Benefits',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'salariesAndEmpBenefits'},
 {'label': 'Cost of Services Provided - Advestising and Sales Promotion + Rent',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'cospMinusAdvertisingPlusRent'},
 {'label': 'Other Operating Exp.',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'otherOperatingExp'},
 {'label': 'EBITDA',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'ebidta'},
 {'label': 'Depreciation/ Amortization',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'depreciationAndAmortization'},
 {'label': 'EBIT',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'pbit'},
 {'label': 'Other Items',
  'state': 'Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'otherItems'},
 {'label': 'Share of Profit/(Loss) of Joint Ventures',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'shareOfProfitLossOfJoinVentures'},
 {'label': 'PBT',
  'state': 'Not Hidden',
  'symbol_when_unhidden': '-',
  'symbol_when_hidden': None,
  'key': 'pbt'},
 {'label': 'Taxes & Other Items',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'taxesAndOtherItems'},
 {'label': 'Net Income',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'netIncome'},
 {'label': 'Diluted EPS',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'dilutedEPS'},
 {'label': 'Basic EPS',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'basicEPS'},
 {'label': 'DPS',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'DPS'},
 {'label': 'Payout Ratio',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'payoutRatio'},
 {'label': 'Cash & Cash Equivalents Investments',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'cashAndCashEquivalents'},
 {'label': 'Long Term Investments',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'longTermInvestments'},
 {'label': 'Loans',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'loans'},
 {'label': 'Other Receivables',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherReceivables'},
 {'label': 'Other Current Assets',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherCurrentAssets'},
 {'label': 'Total Inventory',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'totalInventory'},
 {'label': 'Financial Assets',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'financialAssets'},
 {'label': 'Fixed Assets',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'fixedAssests'},
 {'label': 'Right-of-Use-Asset',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'rightOfUseAsset'},
 {'label': 'Goodwill on consolidation',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'goodWillOnConsolidation'},
 {'label': 'Non-Current Investments',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'nonCurrentInvestments'},
 {'label': 'Deferred Charges',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'deferredCharges'},
 {'label': 'Deferred Tax Assets (Net)',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'deferredTaxAssets'},
 {'label': 'Other Non Current Assets',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'otherNonCurrentAssets'},
 {'label': 'Non Financial Assets',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'nonFinancialAssets'},
 {'label': 'Total Assets',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalAssets'},
 {'label': 'Equity Share Capital',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'equityShareCapital'},
 {'label': 'Reserves & Surplus',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'reservesAndSurplus'},
 {'label': 'Minority Interest',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'minorityInterest'},
 {'label': 'Share Application Money Pending Allotment',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'shareApplicationMoneyPendingAllotment'},
 {'label': 'Other Equity',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'otherEquity'},
 {'label': 'Total Equity',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalEquity'},
 {'label': 'Deposits',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'deposits'},
 {'label': 'Long Term Borrowing',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'longTermBorrowings'},
 {'label': 'Deferred Tax Liabilities',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'deferredTaxLiabilities'},
 {'label': 'Other Financial Liabilities',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherFinancialLiabilities'},
 {'label': 'Other Non Financial Liabilities',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherNonFinancialLiabilities'},
 {'label': 'Short Term Provisions',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'shortTermProvisions'},
 {'label': 'Long Term Provisions',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'longTermProvisions'},
 {'label': 'Short Term Borrowings',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'shortTermBorrowings'},
 {'label': 'Trade Payable',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'tradePayable'},
 {'label': 'Lease Liability',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'leaseLiability'},
 {'label': 'Other Non Current Liability',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherNonCurrentLiabilities'},
 {'label': 'Other Current Liability',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'otherCurrentLiabilities'},
 {'label': 'Current Portion Of Long Term Debt',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'currentPortionOfLongTermDebt'},
 {'label': 'Total Liabilities',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalLiabilities'},
 {'label': "Total Liabilities & Shareholder's Equity",
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalLiabilitiesAndShareHoldingEquity'},
 {'label': 'Total Common Shares Outstanding',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'totalCommonSharesOutstanding'},
 {'label': 'Cash from Operating Activities',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'cashFromOperatingActivities'},
 {'label': 'Cash from Investing Activities',
  'state': 'Hidden',
  'symbol_when_unhidden': '+',
  'symbol_when_hidden': None,
  'key': 'cashFromInvestingActivities'},
 {'label': 'Cash from Financing Activities',
  'state': 'Hidden',
  'symbol_when_unhidden': '=',
  'symbol_when_hidden': None,
  'key': 'cashFromFinancingActivities'},
 {'label': 'Net Change in Cash',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'netChangeInCash'},
 {'label': 'Change in Working Capital',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'changesInWorkingCapital'},
 {'label': 'Capital Expenditures',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'capitalExpenditures'},
 {'label': 'Free Cash Flow',
  'state': 'Not Hidden',
  'symbol_when_unhidden': None,
  'symbol_when_hidden': None,
  'key': 'freeCashFlow'}]

	
	return normal_mapping,nbfc_mapping



def get_3_values(data):
    #data = request.get_json()
    data_list = []
    for each in data:
        data_list.append((each, data[each]))
    length = len(data_list)
    first = data_list[0]
    last = data_list[-1]
    mid = None
    if length%2==1:
        mid = data_list[length//2]
    else:
        mid = data_list[length//2][1] if data_list[length//2][1]>data_list[(length//2)-1] else data_list[(length//2)-1]
        
    response_dict = {first[0]: first[1], mid[0]: mid[1], last[0]: last[1]}

    return response_dict


# @api_view(['GET'])
# def getAllSeedFundingFormObjects(request):
#     per_page = request.GET.get('per_page')
#     q = request.GET.get('q') if request.GET.get('q') else ''
#     object = seedFundingContactUsSignup.objects.filter(
#         Q(contactPerson__icontains=q) | Q(email__icontains=q) | Q(nameOfOrganization__icontains=q))
#     paginator = PageNumberPagination()
#     paginator.page_size = int(per_page) if per_page else 10
#     dataPagination = paginator.paginate_queryset(object, request)
#     serializer_data = seedFundingContactUsSignupSerializer(dataPagination, many=True).data
#     return paginator.get_paginated_response({'data': serializer_data})
#
#     # return Response(serializer.data)
#
# @api_view(['GET'])
# def getAllGrowthFundingFormObject(request):
#     per_page = request.GET.get('per_page')
#     q = request.GET.get('q') if request.GET.get('q') else ''
#     object = growthFundingContactUsSignup.objects.filter(Q(contactPerson__icontains=q) | Q(email__icontains=q) | Q(nameOfOrganization__icontains=q))
#     paginator = PageNumberPagination()
#     paginator.page_size = int(per_page) if per_page else 10
#     dataPagination = paginator.paginate_queryset(object, request)
#     serializer_data = growthFundingContactUsSignupSerializer(dataPagination, many=True).data
#     return paginator.get_paginated_response({'data': serializer_data})
#
# @api_view(['GET'])
# def getAllEarlyFundingFormObject(request):
#     per_page = request.GET.get('per_page')
#     q = request.GET.get('q') if request.GET.get('q') else ''
#     object = earlyFundingContactUsSignup.objects.filter(Q(contactPerson__icontains=q) | Q(email__icontains=q) | Q(nameOfOrganization__icontains=q))
#     paginator = PageNumberPagination()
#     paginator.page_size = int(per_page) if per_page else 10
#     dataPagination = paginator.paginate_queryset(object, request)
#     serializer_data = earlyFundingContactUsSignupSerializer(dataPagination, many=True).data
#     return paginator.get_paginated_response({'data': serializer_data})
#
# @api_view(['GET'])
# def getAllPrivateBoutiqueFormObject(request):
#     per_page = request.GET.get('per_page')
#     q = request.GET.get('q') if request.GET.get('q') else ''
#     object = privateBoutiqueContactUs.objects.filter(Q(name__icontains=q) | Q(email__icontains=q))
#     paginator = PageNumberPagination()
#     paginator.page_size = int(per_page) if per_page else 10
#     dataPagination = paginator.paginate_queryset(object, request)
#     serializer_data = privateBoutiqueContactUsSerializer(dataPagination, many=True).data
#     return paginator.get_paginated_response({'data': serializer_data})
#
# @api_view(['GET'])
# def getAllSellESOPFormObject(request):
#     per_page = request.GET.get('per_page')
#     q = request.GET.get('q') if request.GET.get('q') else ''
#     object = sellESOPContactUs.objects.filter(Q(name__icontains=q)| Q(email__icontains=q)|Q(nameOfOrganization__icontains=q)|Q(websiteURL__icontains=q))
#     paginator = PageNumberPagination()
#     paginator.page_size = int(per_page) if per_page else 10
#     dataPagination = paginator.paginate_queryset(object, request)
#     serializer_data = sellESOPContactUsSerializer(dataPagination, many=True).data
#     return paginator.get_paginated_response({'data': serializer_data})
#
# @api_view(['GET'])
# def getAllSellYourStartupFormObject(request):
#     per_page = request.GET.get('per_page')
#     q = request.GET.get('q') if request.GET.get('q') else ''
#     object = sellYourStartupContactUs.objects.filter(Q(contactPerson__icontains=q)| Q(email__icontains=q)|Q(nameOfOrganization__icontains=q))
#     paginator = PageNumberPagination()
#     paginator.page_size = int(per_page) if per_page else 10
#     dataPagination = paginator.paginate_queryset(object, request)
#     serializer_data = sellYourStartupContactUsSerializer(dataPagination, many=True).data
#     return paginator.get_paginated_response({'data': serializer_data})

@api_view(['GET', 'POST'])
def getFormEntityObject(request):
    if request.method == 'GET':
        queryData = request.GET.get('q', '')
        entity = request.GET.get('entity', '')
        seedFundingData = seedFundingContactUsSignup.objects.filter(
            Q(contactPerson__icontains=queryData) | Q(email__icontains=queryData) | Q(
                nameOfOrganization__icontains=queryData))
        growthFundingData = growthFundingContactUsSignup.objects.filter(
            Q(contactPerson__icontains=queryData) | Q(email__icontains=queryData) | Q(
                nameOfOrganization__icontains=queryData))
        earlyFundingData = earlyFundingContactUsSignup.objects.filter(
            Q(contactPerson__icontains=queryData) | Q(email__icontains=queryData) | Q(
                nameOfOrganization__icontains=queryData))
        privateBoutiqueData = privateBoutiqueContactUs.objects.filter(
            Q(contactPerson__icontains=queryData) | Q(email__icontains=queryData))
        sellEsopData = sellESOPContactUs.objects.filter(Q(contactPerson__icontains=queryData) | Q(email__icontains=queryData) | Q(
            nameOfOrganization__icontains=queryData) | Q(websiteURL__icontains=queryData))
        sellYourStartUpData = sellYourStartupContactUs.objects.filter(
            Q(contactPerson__icontains=queryData) | Q(email__icontains=queryData) | Q(
                nameOfOrganization__icontains=queryData))
        if entity == 'seedFundingContactUsSignup':
            serializer_data = seedFundingContactUsSignupSerializer(seedFundingData, many=True).data

        elif entity == 'growthFundingContactUsSignup':
            serializer_data = growthFundingContactUsSignupSerializer(growthFundingData, many=True).data

        elif entity == 'earlyFundingContactUsSignup':
            serializer_data = earlyFundingContactUsSignupSerializer(earlyFundingData, many=True).data

        elif entity == 'privateBoutiqueContactUs':
            serializer_data = privateBoutiqueContactUsSerializer(privateBoutiqueData, many=True).data

        elif entity == 'sellESOPContactUs':
            serializer_data = sellESOPContactUsSerializer(sellEsopData, many=True).data

        elif entity == 'sellYourStartupContactUs':
            serializer_data = sellYourStartupContactUsSerializer(sellYourStartUpData, many=True).data

        else:
            serializer_data = []
            seedFundingData = seedFundingContactUsSignupSerializer(seedFundingData, many=True).data
            growthFundingData = growthFundingContactUsSignupSerializer(growthFundingData, many=True).data
            earlyFundingData = earlyFundingContactUsSignupSerializer(earlyFundingData, many=True).data
            privateBoutiqueData = privateBoutiqueContactUsSerializer(privateBoutiqueData, many=True).data
            sellEsopData = sellESOPContactUsSerializer(sellEsopData, many=True).data
            sellYourStartUpData = sellYourStartupContactUsSerializer(sellYourStartUpData, many=True).data
            serializer_data+=seedFundingData
            serializer_data+=growthFundingData
            serializer_data+=earlyFundingData
            serializer_data+=privateBoutiqueData
            serializer_data+=sellEsopData
            serializer_data+=sellYourStartUpData
        serializer_data = list(serializer_data)
        serializer_data = sorted(serializer_data, key=lambda d: d['created'], reverse=True)

        employeeUsers = DashboardService.fetch_employee_users()

        for each in serializer_data:
            eachValue = list(each.values())
            userAdvisor = UserAdvisors.objects.filter(identifier=eachValue[1]).first()
            # print(userAdvisor)
            serializedUserAdvisor = UserAdvisorSerializer(userAdvisor).data
            # print(userAdvisor.assigned_advisor_id, serializedUserAdvisor['assigned_advisor_id'])
            advisorData = {}
            if userAdvisor:
                advisorData['advisorId'] = serializedUserAdvisor['assigned_advisor_id']
                if(serializedUserAdvisor['assigned_advisor_id']):
                    advisorData['advisor'] = get_object_or_404(employeePersonalDetails, profileOwner_id=serializedUserAdvisor['assigned_advisor_id']).firstName
                advisorData['comments'] = serializedUserAdvisor['comments']
                advisorData['user_type'] = eachValue[len(eachValue)-1]
            # print(advisorData)
            each.update({'advisorsData': advisorData})

        return Response({'data' : serializer_data, 'employeeUsers': employeeUsers})

    if request.method == 'POST':
        response = DashboardService(request.user).update_user_advisor_data(data=request.data)
        return Response({'response': response})

