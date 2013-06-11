from apps.market_data.models import Orders
from rest_framework import serializers

from eve_db.models.certifications import *
from eve_db.models.chr import *
from eve_db.models.inventory import *
from eve_db.models.map import *
from eve_db.models.npc import *
from eve_db.models.planet import *
from eve_db.models.station import *
from eve_db.models.system import *

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        exclude = ('uploader_ip_hash', 'message_key')

#
# eve_db serializers
#

# Certifications


class CrtCertificateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrtCertificate


class CrtCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrtCategory


class CrtClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrtClass


class CrtRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrtRelationship


class CrtRecommendationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrtRecommendation


# Character

class ChrRaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChrRace


class ChrBloodlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChrBloodline


class ChrAncestrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChrAncestry


class ChrFactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChrFaction


# Inventory

class InvNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvName


class InvMarketGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvMarketGroup


class InvCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvCategory


class InvGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvGroup


class InvMetaGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvMetaGroup


class InvTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvType


class InvTypeMaterialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvTypeMaterial


class InvMetaTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvMetaType


class InvFlagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvFlag


class DgmAttributeCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DgmAttributeCategory


class DgmAttributeTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DgmAttributeType


class DgmTypeAttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DgmTypeAttribute


class InvBlueprintTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvBlueprintType


class DgmEffectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DgmEffect


class DgmTypeEffectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DgmTypeEffect


class InvPOSResourcePurposeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvPOSResourcePurpose


class InvPOSResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvPOSResource


class InvTypeReactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvTypeReaction


class InvContrabandTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvContrabandType


# Map


class MapUniverseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapUniverse


class MapRegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapRegion


class MapRegionJumpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapRegionJump


class MapConstellationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapConstellation


class MapConstellationJumpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapConstellationJump


class MapSolarSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapSolarSystem


class MapSolarSystemJumpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapSolarSystemJump


class MapJumpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapJump


class MapCelestialStatisticSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapCelestialStatistic


class MapDenormalizeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapDenormalize


class MapLandmarkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapLandmark


# NPC


class CrpActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrpActivity


class CrpNPCCorporationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrpNPCCorporation


class CrpNPCDivisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrpNPCDivision


class CrpNPCCorporationDivisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrpNPCCorporationDivision


class CrpNPCCorporationTradeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrpNPCCorporationTrade


class CrpNPCCorporationResearchFieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrpNPCCorporationResearchField


class AgtAgentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AgtAgent


class AgtAgentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AgtAgentType

# Planet


class PlanetSchematicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlanetSchematic


class PlanetSchematicsPinMapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlanetSchematicsPinMap


class PlanetSchematicsTypeMapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlanetSchematicsTypeMap


# Station


class RamActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RamActivity


class RamAssemblyLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RamAssemblyLine


class RamAssemblyLineTypeDetailPerCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RamAssemblyLineTypeDetailPerCategory


class RamAssemblyLineTypeDetailPerGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RamAssemblyLineTypeDetailPerGroup


class RamAssemblyLineStationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RamAssemblyLineStations


class RamTypeRequirementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RamTypeRequirement


class StaServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaService


class StaStationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaStationType


class StaOperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaOperation


class StaStationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaStation


class StaOperationServicesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaOperationServices


# System

class EveUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EveUnit
