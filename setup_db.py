import db as DB


db, mydb = DB.get_main()

def initialize():
    
    db.execute(         # Users (id, name, xp, tier, lun, lun_tokens)
        f"create table if not exists users (id bigint not null primary key, name varchar(100) not null, xp int not null default 0, tier varchar(255), lun bigint not null default 0, lun_tokens float not null default 0)"
    )
    mydb.commit()
    
    
    db.execute(         # Players (id, name, hp, energy, armor, moves)
        f"create table if not exists players (id bigint not null primary key, name varchar(100) not null, hp int not null default 100, energy int not null default 75, armor int not null default 0, moves varchar(255) not null default 'strike/pounce/defend')"
    )
    mydb.commit()
    
    
    db.execute(         # Inv (id, items, amounts)
        f"create table if not exists inv (id bigint not null primary key, items varchar(255), amounts varchar(255))"
    )
    mydb.commit()
    
    
    db.execute(f"select * from pools")
    pools = db.fetchall()
    pools_data = [
            ('jackpot_gamble', 50000),
            ('jackpot_slots', 50000)
        ]
    if len(pools) != len(pools_data):
        db.execute(f"drop table if exists pools")
        mydb.commit()
        db.execute(         # Pools (name, balance)
                f"create table if not exists pools (name varchar(100) not null primary key, balance bigint not null default 50000)"
            )
        mydb.commit()
        sql = 'insert into pools (name, balance) values(?, ?)'
        db.executemany(sql, pools_data)
        mydb.commit()
    
    db.execute(f"select * from supply")
    supply = db.fetchall()
    supply_data = [
            ('lun', 100000000)
        ]
    if len(supply) != len(supply_data):
        db.execute(f"drop table if exists supply")
        mydb.commit()
        db.execute(         # Supply (name, total, circulating)
                f"create table if not exists supply (name varchar(100) not null primary key, total bigint not null default 100000000, circulating bigint not null default 0)"
            )
        mydb.commit()
        sql = 'insert into supply (name, total) values(?, ?)'
        db.executemany(sql, supply_data)
        mydb.commit()
    
    db.execute(f"select * from items")
    items = db.fetchall()
    items_data = [
            (1, 'lun', 1),
            (2, 'lun_token', 400000)
        ]
    if len(items) != len(items_data):
        db.execute(f"drop table if exists items")
        mydb.commit()
        db.execute(         # Items (id, name, lun_price, lt_price, luni_value)
                f"create table if not exists items (id int not null primary key, name varchar(100) not null, lun_price bigint not null default 0, lt_price bigint not null default 0, luni_value float not null default 0)"
            )
        mydb.commit()
        sql = 'insert into items (id, name, lun_price) values(?, ?, ?)'
        db.executemany(sql, items_data)
        mydb.commit()