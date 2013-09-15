from django.utils.datastructures import SortedDict

from rest_framework.views import get_view_name, get_view_description
from rest_framework import viewsets

from apps.market_data.models import Orders, OrderHistory, ItemRegionStat

from apps.rest_api.serializers import *
from apps.rest_api.filters import *


#
# market_data views
#


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows orders to be viewed and filtered.
    """

    queryset = Orders.active.all()
    serializer_class = OrderSerializer
    filter_class = OrdersFilter

    def metadata(self, request):
        """
        Return a dictionary of metadata about the view.
        Used to return responses for OPTIONS requests.
        """

        # This is used by ViewSets to disambiguate instance vs list views
        view_name_suffix = getattr(self, 'suffix', None)

        # By default we can't provide any form-like information, however the
        # generic views override this implementation and add additional
        # information for POST and PUT methods, based on the serializer.
        ret = SortedDict()
        ret['name'] = get_view_name(self.__class__, view_name_suffix)
        ret['description'] = get_view_description(self.__class__)
        ret['renders'] = [renderer.media_type for renderer in self.renderer_classes]
        ret['parses'] = [parser.media_type for parser in self.parser_classes]
        ret['filters'] = OrdersFilter.Meta.fields
        return ret


class ItemRegionStatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows the current regional stats of an item to be viewed and filtered.
    """

    queryset = ItemRegionStat.objects.all()
    serializer_class = ItemRegionStatSerializer
    filter_class = ItemRegionStatFilter

    def metadata(self, request):
        """
        Return a dictionary of metadata about the view.
        Used to return responses for OPTIONS requests.
        """

        # This is used by ViewSets to disambiguate instance vs list views
        view_name_suffix = getattr(self, 'suffix', None)

        # By default we can't provide any form-like information, however the
        # generic views override this implementation and add additional
        # information for POST and PUT methods, based on the serializer.
        ret = SortedDict()
        ret['name'] = get_view_name(self.__class__, view_name_suffix)
        ret['description'] = get_view_description(self.__class__)
        ret['renders'] = [renderer.media_type for renderer in self.renderer_classes]
        ret['parses'] = [parser.media_type for parser in self.parser_classes]
        ret['filters'] = ItemRegionStatFilter.Meta.fields
        return ret


class OrderHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows past regional stats of an item to be viewed and filtered.
    """

    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer
    filter_class = OrderHistoryFilter

    def metadata(self, request):
        """
        Return a dictionary of metadata about the view.
        Used to return responses for OPTIONS requests.
        """

        # This is used by ViewSets to disambiguate instance vs list views
        view_name_suffix = getattr(self, 'suffix', None)

        # By default we can't provide any form-like information, however the
        # generic views override this implementation and add additional
        # information for POST and PUT methods, based on the serializer.
        ret = SortedDict()
        ret['name'] = get_view_name(self.__class__, view_name_suffix)
        ret['description'] = get_view_description(self.__class__)
        ret['renders'] = [renderer.media_type for renderer in self.renderer_classes]
        ret['parses'] = [parser.media_type for parser in self.parser_classes]
        ret['filters'] = OrderHistoryFilter.Meta.fields
        return ret


#
# eve_db views
#

# Certifications

class CrtCertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrtCertificates to be viewed.
    """

    queryset = CrtCertificate.objects.all()
    serializer_class = CrtCertificateSerializer


class CrtCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrtCategories to be viewed.
    """

    queryset = CrtCategory.objects.all()
    serializer_class = CrtCategorySerializer


class CrtClassViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrtClasss to be viewed.
    """

    queryset = CrtClass.objects.all()
    serializer_class = CrtClassSerializer


class CrtRelationshipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrtRelationships to be viewed.
    """

    queryset = CrtRelationship.objects.all()
    serializer_class = CrtRelationshipSerializer


class CrtRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrtRecommendations to be viewed.
    """

    queryset = CrtRecommendation.objects.all()
    serializer_class = CrtRecommendationSerializer

# Character


class ChrRaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows ChrRaces to be viewed.
    """

    queryset = ChrRace.objects.all()
    serializer_class = ChrRaceSerializer


class ChrBloodlineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows ChrBloodlines to be viewed.
    """

    queryset = ChrBloodline.objects.all()
    serializer_class = ChrBloodlineSerializer


class ChrAncestryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows ChrAncestrys to be viewed.
    """

    queryset = ChrAncestry.objects.all()
    serializer_class = ChrAncestrySerializer


class ChrFactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows ChrFactions to be viewed.
    """

    queryset = ChrFaction.objects.all()
    serializer_class = ChrFactionSerializer

# Inventory


class InvNameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvNames to be viewed.
    """

    queryset = InvName.objects.all()
    serializer_class = InvNameSerializer


class InvMarketGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvMarketGroups to be viewed.
    """

    queryset = InvMarketGroup.objects.all()
    serializer_class = InvMarketGroupSerializer


class InvCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvCategorys to be viewed.
    """

    queryset = InvCategory.objects.all()
    serializer_class = InvCategorySerializer


class InvGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvGroups to be viewed.
    """

    queryset = InvGroup.objects.all()
    serializer_class = InvGroupSerializer


class InvMetaGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvMetaGroups to be viewed.
    """

    queryset = InvMetaGroup.objects.all()
    serializer_class = InvMetaGroupSerializer


class InvTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvTypes to be viewed.
    """

    queryset = InvType.objects.all()
    serializer_class = InvTypeSerializer


class InvTypeMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvTypeMaterials to be viewed.
    """

    queryset = InvTypeMaterial.objects.all()
    serializer_class = InvTypeMaterialSerializer


class InvMetaTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvMetaTypes to be viewed.
    """

    queryset = InvMetaType.objects.all()
    serializer_class = InvMetaTypeSerializer


class InvFlagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvFlags to be viewed.
    """

    queryset = InvFlag.objects.all()
    serializer_class = InvFlagSerializer


class DgmAttributeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows DgmAttributeCategorys to be viewed.
    """

    queryset = DgmAttributeCategory.objects.all()
    serializer_class = DgmAttributeCategorySerializer


class DgmAttributeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows DgmAttributeTypes to be viewed.
    """

    queryset = DgmAttributeType.objects.all()
    serializer_class = DgmAttributeTypeSerializer


class DgmTypeAttributeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows DgmTypeAttributes to be viewed.
    """

    queryset = DgmTypeAttribute.objects.all()
    serializer_class = DgmTypeAttributeSerializer


class InvBlueprintTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvBlueprintTypes to be viewed.
    """

    queryset = InvBlueprintType.objects.all()
    serializer_class = InvBlueprintTypeSerializer


class DgmEffectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows DgmEffects to be viewed.
    """

    queryset = DgmEffect.objects.all()
    serializer_class = DgmEffectSerializer


class DgmTypeEffectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows DgmTypeEffects to be viewed.
    """

    queryset = DgmTypeEffect.objects.all()
    serializer_class = DgmTypeEffectSerializer


class InvPOSResourcePurposeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvPOSResourcePurposes to be viewed.
    """

    queryset = InvPOSResourcePurpose.objects.all()
    serializer_class = InvPOSResourcePurposeSerializer


class InvPOSResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvPOSResources to be viewed.
    """

    queryset = InvPOSResource.objects.all()
    serializer_class = InvPOSResourceSerializer


class InvTypeReactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvTypeReactions to be viewed.
    """

    queryset = InvTypeReaction.objects.all()
    serializer_class = InvTypeReactionSerializer


class InvContrabandTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows InvContrabandTypes to be viewed.
    """

    queryset = InvContrabandType.objects.all()
    serializer_class = InvContrabandTypeSerializer

# Map


class MapUniverseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapUniverses to be viewed.
    """

    queryset = MapUniverse.objects.all()
    serializer_class = MapUniverseSerializer


class MapRegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapRegions to be viewed.
    """

    queryset = MapRegion.objects.all()
    serializer_class = MapRegionSerializer


class MapRegionJumpViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapRegionJumps to be viewed.
    """

    queryset = MapRegionJump.objects.all()
    serializer_class = MapRegionJumpSerializer


class MapConstellationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapConstellations to be viewed.
    """

    queryset = MapConstellation.objects.all()
    serializer_class = MapConstellationSerializer


class MapConstellationJumpViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapConstellationJumps to be viewed.
    """

    queryset = MapConstellationJump.objects.all()
    serializer_class = MapConstellationJumpSerializer


class MapSolarSystemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapSolarSystems to be viewed.
    """

    queryset = MapSolarSystem.objects.all()
    serializer_class = MapSolarSystemSerializer


class MapSolarSystemJumpViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapSolarSystemJumps to be viewed.
    """

    queryset = MapSolarSystemJump.objects.all()
    serializer_class = MapSolarSystemJumpSerializer


class MapJumpViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapJumps to be viewed.
    """

    queryset = MapJump.objects.all()
    serializer_class = MapJumpSerializer


class MapCelestialStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapCelestialStatistics to be viewed.
    """

    queryset = MapCelestialStatistic.objects.all()
    serializer_class = MapCelestialStatisticSerializer


class MapDenormalizeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapDenormalizes to be viewed.
    """

    queryset = MapDenormalize.objects.all()
    serializer_class = MapDenormalizeSerializer


class MapLandmarkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows MapLandmarks to be viewed.
    """

    queryset = MapLandmark.objects.all()
    serializer_class = MapLandmarkSerializer


# NPC


class CrpActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrpActivitys to be viewed.
    """

    queryset = CrpActivity.objects.all()
    serializer_class = CrpActivitySerializer


class CrpNPCCorporationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrpNPCCorporations to be viewed.
    """

    queryset = CrpNPCCorporation.objects.all()
    serializer_class = CrpNPCCorporationSerializer


class CrpNPCCorporationDivisionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrpNPCCorporationDivisions to be viewed.
    """

    queryset = CrpNPCCorporationDivision.objects.all()
    serializer_class = CrpNPCCorporationDivisionSerializer


class CrpNPCDivisionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrpNPCDivisions to be viewed.
    """

    queryset = CrpNPCDivision.objects.all()
    serializer_class = CrpNPCDivisionSerializer


class CrpNPCCorporationTradeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrpNPCCorporationTrades to be viewed.
    """

    queryset = CrpNPCCorporationTrade.objects.all()
    serializer_class = CrpNPCCorporationTradeSerializer


class CrpNPCCorporationResearchFieldViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows CrpNPCCorporationResearchFields to be viewed.
    """

    queryset = CrpNPCCorporationResearchField.objects.all()
    serializer_class = CrpNPCCorporationResearchFieldSerializer


class AgtAgentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows AgtAgents to be viewed.
    """

    queryset = AgtAgent.objects.all()
    serializer_class = AgtAgentSerializer


class AgtAgentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows AgtAgentTypes to be viewed.
    """

    queryset = AgtAgentType.objects.all()
    serializer_class = AgtAgentTypeSerializer


# Planet


class PlanetSchematicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows PlanetSchematics to be viewed.
    """

    queryset = PlanetSchematic.objects.all()
    serializer_class = PlanetSchematicSerializer


class PlanetSchematicsPinMapViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows PlanetSchematicsPinMaps to be viewed.
    """

    queryset = PlanetSchematicsPinMap.objects.all()
    serializer_class = PlanetSchematicsPinMapSerializer


class PlanetSchematicsTypeMapViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows PlanetSchematicsTypeMaps to be viewed.
    """

    queryset = PlanetSchematicsTypeMap.objects.all()
    serializer_class = PlanetSchematicsTypeMapSerializer


# Station


class RamActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows RamActivities to be viewed.
    """

    queryset = RamActivity.objects.all()
    serializer_class = RamActivitySerializer


class RamAssemblyLineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows RamAssemblyLines to be viewed.
    """

    queryset = RamAssemblyLine.objects.all()
    serializer_class = RamAssemblyLineSerializer


class RamAssemblyLineTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows RamAssemblyLineTypes to be viewed.
    """

    queryset = RamAssemblyLineType.objects.all()
    serializer_class = RamAssemblyLineTypeSerializer


class RamAssemblyLineTypeDetailPerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows RamAssemblyLineTypeDetailPerCategories to be viewed.
    """

    queryset = RamAssemblyLineTypeDetailPerCategory.objects.all()
    serializer_class = RamAssemblyLineTypeDetailPerCategorySerializer


class RamAssemblyLineTypeDetailPerGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows RamAssemblyLineTypeDetailPerGroups to be viewed.
    """

    queryset = RamAssemblyLineTypeDetailPerGroup.objects.all()
    serializer_class = RamAssemblyLineTypeDetailPerGroupSerializer


class RamAssemblyLineStationsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows RamAssemblyLineStationss to be viewed.
    """

    queryset = RamAssemblyLineStations.objects.all()
    serializer_class = RamAssemblyLineStationsSerializer


class RamTypeRequirementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows RamTypeRequirements to be viewed.
    """

    queryset = RamTypeRequirement.objects.all()
    serializer_class = RamTypeRequirementSerializer


class StaServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows StaServices to be viewed.
    """

    queryset = StaService.objects.all()
    serializer_class = StaServiceSerializer


class StaStationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows StaStations to be viewed.
    """

    queryset = StaStation.objects.all()
    serializer_class = StaStationSerializer


class StaOperationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows StaOperations to be viewed.
    """

    queryset = StaOperation.objects.all()
    serializer_class = StaOperationSerializer


class StaStationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows StaStationTypes to be viewed.
    """

    queryset = StaStationType.objects.all()
    serializer_class = StaStationTypeSerializer


class StaOperationServicesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows StaOperationServicess to be viewed.
    """

    queryset = StaOperationServices.objects.all()
    serializer_class = StaOperationServicesSerializer


# System


class EveUnitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows EveUnits to be viewed.
    """

    queryset = EveUnit.objects.all()
    serializer_class = EveUnitSerializer
