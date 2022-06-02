from sqlalchemy import create_engine, Table, Column, String, Float, MetaData

def DumpToSqlLite(data):
    ###
    # Here, we are using default engine of sqline and creating tables in the sqlife for the mapping part
    ###
    dbEngine = create_engine('sqlite:///{}.db'.format("ResultSet"), echo=False)
    metadata = MetaData(dbEngine)

    mappingTableSchema = Table('testMappingData', metadata,
                    Column('X (test function)', Float, primary_key=False),
                    Column('Y (test function)', Float),
                    Column('Delta Y', Float),
                    Column('Name of ideal function', String(20))
                    )

    metadata.create_all()

    tableData = []
    for singleRaw in data:
        point = singleRaw["point"]
        bestFunction = singleRaw["classification"]
        yDelta = singleRaw["delta_y"]

        if bestFunction is not None:
            bestFunctionName = bestFunction['BestFunction']['BestFunction'].name
        else:
            # If there is no classification, there is also no distance. In that case I write a dash
            bestFunctionName = "-"
            yDelta = -1

        # Make sure the column name should be same as table schema, otherwise it will thorw an error
        tableData.append(
            {"X (test function)": point["x"], "Y (test function)": point["y"], "Delta Y": yDelta,
             "Name of ideal function": bestFunctionName})

    # here we are inserting data and executing the query
    query = mappingTableSchema.insert()
    query.execute(tableData)
