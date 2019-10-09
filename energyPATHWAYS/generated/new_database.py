from csvdb import CsvMetadata, CsvDatabase
from energyPATHWAYS.generated.text_mappings import MappedCols

_Metadata = [
    CsvMetadata('BlendNodeBlendMeasures',
                key_col='name',
                df_cols=['gau', 'demand_sector', 'value', 'year']),
    CsvMetadata('BlendNodeInputsData',
                data_table=True),
    CsvMetadata('CO2PriceMeasures',
                key_col='name',
                lowcase_cols=['sensitivity'],
                df_cols=['gau', 'sensitivity', 'value', 'year']),
    CsvMetadata('CurrenciesConversion',
                data_table=True),
    CsvMetadata('DemandCO2CaptureMeasures',
                data_table=True),
    CsvMetadata('DemandDrivers',
                key_col='name',
                lowcase_cols=['sensitivity'],
                df_cols=['gau', 'value', 'oth_2', 'oth_1', 'year', 'sensitivity']),
    CsvMetadata('DemandEnergyDemands',
                key_col='subsector',
                lowcase_cols=['sensitivity'],
                df_cols=['gau', 'demand_technology', 'value', 'oth_2', 'oth_1', 'year', 'final_energy', 'sensitivity']),
    CsvMetadata('DemandEnergyEfficiencyMeasures',
                key_col='name',
                df_cols=['gau', 'value', 'oth_2', 'oth_1', 'year', 'final_energy']),
    CsvMetadata('DemandEnergyEfficiencyMeasuresCost',
                key_col='parent',
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'final_energy']),
    CsvMetadata('DemandFlexibleLoadMeasures',
                key_col='name',
                df_cols=['gau', 'demand_technology', 'value', 'oth_1', 'year']),
    CsvMetadata('DemandFuelSwitchingMeasures',
                key_col='name'),
    CsvMetadata('DemandFuelSwitchingMeasuresCost',
                key_col='parent',
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1']),
    CsvMetadata('DemandFuelSwitchingMeasuresEnergyIntensity',
                key_col='parent',
                df_cols=['gau', 'value', 'oth_2', 'oth_1', 'year']),
    CsvMetadata('DemandFuelSwitchingMeasuresImpact',
                key_col='parent',
                df_cols=['gau', 'value', 'oth_2', 'oth_1', 'year']),
    CsvMetadata('DemandSales',
                key_col='demand_technology',
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1']),
    CsvMetadata('DemandSalesShareMeasures',
                key_col='name',
                df_cols=['vintage', 'gau', 'oth_1', 'value']),
    CsvMetadata('DemandSectors',
                key_col='name'),
    CsvMetadata('DemandServiceDemandMeasures',
                key_col='name',
                df_cols=['gau', 'value', 'oth_2', 'oth_1', 'year']),
    CsvMetadata('DemandServiceDemandMeasuresCost',
                key_col='parent',
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1']),
    CsvMetadata('DemandServiceDemands',
                key_col='subsector',
                lowcase_cols=['sensitivity'],
                df_cols=['gau', 'demand_technology', 'value', 'oth_2', 'oth_1', 'year', 'final_energy', 'sensitivity']),
    CsvMetadata('DemandServiceEfficiency',
                key_col='subsector',
                df_cols=['gau', 'value', 'oth_2', 'oth_1', 'year', 'final_energy']),
    CsvMetadata('DemandServiceLink',
                key_col='name'),
    CsvMetadata('DemandStock',
                key_col='subsector',
                df_cols=['gau', 'demand_technology', 'value', 'oth_2', 'oth_1', 'year']),
    CsvMetadata('DemandStockMeasures',
                key_col='name',
                df_cols=['gau', 'oth_1', 'value', 'year']),
    CsvMetadata('DemandSubsectors',
                key_col='name'),
    CsvMetadata('DemandTechs',
                key_col='name'),
    CsvMetadata('DemandTechsAuxEfficiency',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'sensitivity']),
    CsvMetadata('DemandTechsCapitalCost',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'sensitivity']),
    CsvMetadata('DemandTechsFixedMaintenanceCost',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'sensitivity']),
    CsvMetadata('DemandTechsFuelSwitchCost',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'sensitivity']),
    CsvMetadata('DemandTechsInstallationCost',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'sensitivity']),
    CsvMetadata('DemandTechsMainEfficiency',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'sensitivity']),
    CsvMetadata('DemandTechsParasiticEnergy',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'final_energy', 'sensitivity']),
    CsvMetadata('DemandTechsServiceDemandModifier',
                key_col='demand_technology',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'gau', 'value', 'oth_2', 'oth_1', 'sensitivity']),
    CsvMetadata('DemandTechsServiceLink',
                key_col='name',
                df_cols=['vintage', 'gau', 'oth_1', 'oth_2', 'value']),
    CsvMetadata('DispatchFeedersAllocation',
                key_col='name',
                df_cols=['gau', 'year', 'value', 'dispatch_feeder', 'demand_sector']),
    CsvMetadata('DispatchNodeConfig',
                key_col='supply_node'),
    CsvMetadata('DispatchTransmissionConstraint',
                key_col='name',
                lowcase_cols=['sensitivity'],
                df_cols=['gau_to', 'gau_from', 'hour', 'sensitivity', 'value', 'month', 'day_type', 'year']),
    CsvMetadata('DispatchTransmissionCost',
                key_col='name',
                lowcase_cols=['sensitivity'],
                drop_cols=['source', 'notes'],
                df_cols=['gau_to', 'gau_from', 'sensitivity', 'value','year']),

    CsvMetadata('DispatchTransmissionHurdleRate',
                key_col='name',
                lowcase_cols=['sensitivity'],
                df_cols=['gau_to', 'gau_from', 'hour', 'sensitivity', 'value', 'month', 'day_type', 'year']),
    CsvMetadata('DispatchTransmissionLosses',
                key_col='name',
                lowcase_cols=['sensitivity'],
                df_cols=['gau_to', 'gau_from', 'hour', 'sensitivity', 'value', 'month', 'day_type', 'year']),
    CsvMetadata('FinalEnergy',
                data_table=True),
    CsvMetadata('Geographies',
                data_table=True),
    CsvMetadata('GeographiesSpatialJoin',
                data_table=True),
    CsvMetadata('GeographyMapKeys',
                data_table=True),
    CsvMetadata('GreenhouseGases',
                data_table=True),
    CsvMetadata('IDMap',
                data_table=True),
    CsvMetadata('ImportCost',
                key_col='import_node',
                lowcase_cols=['sensitivity'],
                df_cols=['sensitivity', 'demand_sector', 'value', 'resource_bin', 'year', 'gau']),
    CsvMetadata('IndexLevels',
                data_table=True),
    CsvMetadata('InflationConversion',
                data_table=True),
    CsvMetadata('OtherIndexes',
                data_table=True),
    CsvMetadata('OtherIndexesData_copy',
                data_table=True),
    CsvMetadata('PrimaryCost',
                key_col='primary_node',
                lowcase_cols=['sensitivity'],
                df_cols=['sensitivity', 'year', 'value', 'resource_bin', 'oth_1', 'demand_sector', 'gau']),
    CsvMetadata('Shapes',
                data_table=True),
    CsvMetadata('StorageTechsDuration',
                key_col='supply_tech',
                lowcase_cols=['sensitivity'],
                df_cols=['gau', 'value', 'oth_2', 'oth_1', 'year', 'sensitivity']),
    CsvMetadata('SupplyCapacityFactor',
                key_col='supply_node',
                df_cols=['gau', 'demand_sector', 'value', 'resource_bin', 'year']),
    CsvMetadata('SupplyCost',
                key_col='name',
                lowcase_cols=['sensitivity'],
                df_cols=['sensitivity', 'demand_sector', 'value', 'resource_bin', 'year', 'gau']),
    CsvMetadata('SupplyEfficiency',
                key_col='name',
                lowcase_cols=['sensitivity'],
                df_cols=['efficiency_type', 'sensitivity', 'demand_sector', 'value', 'resource_bin', 'year', 'supply_node', 'gau']),
    CsvMetadata('SupplyEmissions',
                key_col='supply_node',
                lowcase_cols=['sensitivity'],
                df_cols=['gau', 'demand_sector', 'value', 'ghg', 'oth_1', 'year', 'sensitivity', 'ghg_type']),
    CsvMetadata('SupplyExport',
                key_col='supply_node',
                df_cols=['gau', 'value', 'resource_bin', 'oth_1', 'year']),
    CsvMetadata('SupplyExportMeasures',
                key_col='name',
                df_cols=['gau', 'oth_1', 'value', 'year']),
    CsvMetadata('SupplyNodes',
                key_col='name'),
    CsvMetadata('SupplyPotential',
                key_col='supply_node',
                lowcase_cols=['sensitivity'],
                df_cols=['gau', 'year', 'value', 'resource_bin', 'oth_1', 'demand_sector', 'sensitivity']),
    CsvMetadata('SupplyPotentialConversion',
                key_col='supply_node',
                df_cols=['gau', 'value', 'resource_bin', 'oth_1', 'year']),
    CsvMetadata('SupplySales',
                key_col='supply_technology',
                df_cols=['vintage', 'gau', 'value', 'resource_bin', 'demand_sector']),
    CsvMetadata('SupplySalesMeasures',
                key_col='name',
                df_cols=['vintage', 'gau', 'value', 'resource_bin', 'oth_1', 'demand_sector']),
    CsvMetadata('SupplySalesShare',
                key_col='supply_technology',
                df_cols=['vintage', 'gau', 'value', 'demand_sector']),
    CsvMetadata('SupplySalesShareMeasures',
                key_col='name',
                df_cols=['vintage', 'gau', 'value', 'resource_bin', 'oth_1', 'demand_sector']),
    CsvMetadata('SupplyStock',
                key_col='supply_node',
                lowcase_cols=['sensitivity'],
                df_cols=['sensitivity', 'demand_sector', 'value', 'resource_bin', 'year', 'supply_technology', 'gau']),
    CsvMetadata('SupplyStockMeasures',
                key_col='name',
                df_cols=['gau', 'demand_sector', 'value', 'resource_bin', 'oth_1', 'year']),
    CsvMetadata('SupplyTechs',
                key_col='name'),
    CsvMetadata('SupplyTechsCO2Capture',
                key_col='supply_tech',
                df_cols=['vintage', 'gau', 'resource_bin', 'value']),
    CsvMetadata('SupplyTechsCapacityFactor',
                key_col='supply_tech',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'sensitivity', 'value', 'resource_bin', 'oth_1', 'gau']),
    CsvMetadata('SupplyTechsCapitalCost',
                key_col='supply_tech',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'sensitivity', 'value', 'resource_bin', 'demand_sector', 'gau']),
    CsvMetadata('SupplyTechsEfficiency',
                key_col='supply_tech',
                lowcase_cols=['sensitivity'],
                df_cols=['efficiency_type', 'vintage', 'sensitivity', 'value', 'resource_bin', 'demand_sector', 'supply_node', 'gau']),
    CsvMetadata('SupplyTechsFixedMaintenanceCost',
                key_col='supply_tech',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'sensitivity', 'value', 'resource_bin', 'demand_sector', 'gau']),
    CsvMetadata('SupplyTechsInstallationCost',
                key_col='supply_tech',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'sensitivity', 'value', 'resource_bin', 'demand_sector', 'gau']),
    CsvMetadata('SupplyTechsVariableMaintenanceCost',
                key_col='supply_tech',
                lowcase_cols=['sensitivity'],
                df_cols=['vintage', 'sensitivity', 'value', 'resource_bin', 'demand_sector', 'gau']),
    CsvMetadata('TimeZones',
                data_table=True),
    CsvMetadata('Version',
                data_table=True),
    CsvMetadata('foreign_keys',
                data_table=True),
]

class EnergyPathwaysDatabase(CsvDatabase):
    def __init__(self, pathname=None, load=True, output_tables=False, compile_sensitivities=False, tables_to_not_load=None):
        super(EnergyPathwaysDatabase, self).__init__(
            metadata=_Metadata,
            pathname=pathname,
            load=load,
            mapped_cols=None,
            output_tables=output_tables,
            compile_sensitivities=compile_sensitivities,
            tables_to_not_load=tables_to_not_load,
            tables_without_classes=['CurrenciesConversion', 'GeographyMap', 'IDMap', 'InflationConversion', 'Version', 'foreign_keys'],
            tables_to_ignore=['CurrencyYears', 'DispatchConfig', 'GeographyIntersection', 'GeographyIntersectionData', 'GeographyMap', 'GeographiesSpatialJoin'])