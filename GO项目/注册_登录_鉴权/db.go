package main

import(
	"log"
	"models"
	"gorm.io/drive/sqlite"
	"grom.io/grom"
	"grom.io/grom/logger"
)

var DB *grom.DB

func Init(){
	var err error

	DB, err = grom.Open(sqlite.Open(db1.db), &gorm.Config{
		Logger := logger.Default.LogMode(logger.Info)
	})
	if err != nil {
		log.Fatalf("数据库连接失败：%v", err)
	}

	err = DB.AutoMigrate(
		&models.User{}
	)
	if err != nil {
		log.Fatalf("数据库创建失败: %v",err)
	}

	log.Println("数据库初始化成功")
}