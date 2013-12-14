from django.conf.urls import patterns, url, include
from rest_framework import routers

from apps.rest_api import views

router = routers.DefaultRouter()


#
# market_data routes
#

router.register(r'order', views.OrderViewSet)
router.register(r'itemRegionStat', views.ItemRegionStatViewSet)
router.register(r'orderHistory', views.OrderHistoryViewSet)

#
# eve_db routes
#

# Character

router.register(r'chrRace', views.ChrRaceViewSet)
router.register(r'chrBloodline', views.ChrBloodlineViewSet)
router.register(r'chrAncestry', views.ChrAncestryViewSet)
router.register(r'chrFaction', views.ChrFactionViewSet)

# Inventory

router.register(r'invName', views.InvNameViewSet)
router.register(r'invMarketGroup', views.InvMarketGroupViewSet)
router.register(r'invCategory', views.InvCategoryViewSet)
router.register(r'invGroup', views.InvGroupViewSet)
router.register(r'invMetaGroup', views.InvMetaGroupViewSet)
router.register(r'invType', views.InvTypeViewSet)
router.register(r'invTypeMaterial', views.InvTypeMaterialViewSet)
router.register(r'invMetaType', views.InvMetaTypeViewSet)
router.register(r'invFlag', views.InvFlagViewSet)
router.register(r'dgmAttributeCategory', views.DgmAttributeCategoryViewSet)
router.register(r'dgmAttributeType', views.DgmAttributeTypeViewSet)
router.register(r'dgmTypeAttribute', views.DgmTypeAttributeViewSet)
router.register(r'invBlueprintType', views.InvBlueprintTypeViewSet)
router.register(r'dgmEffect', views.DgmEffectViewSet)
router.register(r'dgmTypeEffect', views.DgmTypeEffectViewSet)
router.register(r'invPOSResourcePurpose', views.InvPOSResourcePurposeViewSet)
router.register(r'invPOSResource', views.InvPOSResourceViewSet)
router.register(r'invTypeReaction', views.InvTypeReactionViewSet)
router.register(r'invContrabandType', views.InvContrabandTypeViewSet)
router.register(r'invItem', views.InvItemViewSet)
router.register(r'invPosition', views.InvPositionViewSet)
router.register(r'invUniqueName', views.InvUniqueNameViewSet)

# Map

router.register(r'mapUniverse', views.MapUniverseViewSet)
router.register(r'mapRegion', views.MapRegionViewSet)
router.register(r'mapRegionJump', views.MapRegionJumpViewSet)
router.register(r'mapConstellation', views.MapConstellationViewSet)
router.register(r'mapConstellationJump', views.MapConstellationJumpViewSet)
router.register(r'mapSolarSystem', views.MapSolarSystemViewSet)
router.register(r'mapSolarSystemJump', views.MapSolarSystemJumpViewSet)
router.register(r'mapJump', views.MapJumpViewSet)
router.register(r'mapCelestialStatistic', views.MapCelestialStatisticViewSet)
router.register(r'mapDenormalize', views.MapDenormalizeViewSet)
router.register(r'mapLandmark', views.MapLandmarkViewSet)
router.register(r'mapLocationScene', views.MapLocationSceneViewSet)
router.register(r'mapLocationWormholeClass', views.MapLocationWormholeClassViewSet)
router.register(r'warCombatZone', views.WarCombatZoneViewSet)
router.register(r'warCombatZoneSystem', views.WarCombatZoneSystemViewSet)

# NPC

router.register(r'crpActivity', views.CrpActivityViewSet)
router.register(r'crpNPCCorporation', views.CrpNPCCorporationViewSet)
router.register(r'crpNPCDivision', views.CrpNPCDivisionViewSet)
router.register(r'crpNPCCorporationDivision', views.CrpNPCCorporationDivisionViewSet)
router.register(r'crpNPCCorporationTrade', views.CrpNPCCorporationTradeViewSet)
router.register(r'crpNPCCorporationResearchField', views.CrpNPCCorporationResearchFieldViewSet)
router.register(r'agtAgent', views.AgtAgentViewSet)
router.register(r'agtAgentType', views.AgtAgentTypeViewSet)
router.register(r'agtResearchAgent', views.AgtResearchAgentViewSet)

# Planet

router.register(r'planetSchematic', views.PlanetSchematicViewSet)
router.register(r'planetSchematicsPinMap', views.PlanetSchematicsPinMapViewSet)
router.register(r'planetSchematicsTypeMap', views.PlanetSchematicsTypeMapViewSet)


# Station

router.register(r'ramActivity', views.RamActivityViewSet)
router.register(r'ramAssemblyLine', views.RamAssemblyLineViewSet)
router.register(r'ramAssemblyLineType', views.RamAssemblyLineTypeViewSet)
router.register(r'ramAssemblyLineTypeDetailPerCategory', views.RamAssemblyLineTypeDetailPerCategoryViewSet)
router.register(r'ramAssemblyLineTypeDetailPerGroup', views.RamAssemblyLineTypeDetailPerGroupViewSet)
router.register(r'ramAssemblyLineStations', views.RamAssemblyLineStationsViewSet)
router.register(r'ramTypeRequirement', views.RamTypeRequirementViewSet)
router.register(r'staService', views.StaServiceViewSet)
router.register(r'staStation', views.StaStationViewSet)
router.register(r'staStationType', views.StaStationTypeViewSet)
router.register(r'staOperation', views.StaOperationViewSet)
router.register(r'staStation', views.StaStationViewSet)
router.register(r'staOperationServices', views.StaOperationServicesViewSet)
router.register(r'ramInstallationTypeContent', views.RamInstallationTypeContentViewSet)

# System

router.register(r'eveUnit', views.EveUnitViewSet)


urlpatterns = patterns('',
    #
    # REST API URLs
    #

    url(r'^', include(router.urls)),

    url(r'', include('rest_framework.urls', namespace='rest_framework')),
)
