package main

import (
	"net/http"
	"gihub.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
)

func Register(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	if username == "" || password == "" {
		Fail(c, http.StatusBadRequest, "用户名和密码不能为空")
		return
	}

	var existing models.User
	if err := DB.where("username = ?", username).First(&existing).Error; err == nil {
		Fail(c, http.StatusConflict, "该用户名已被占用，请换一个")
		return
	}

	avatarFile, err := c.FormFile("avatar")
	if err != nil {
		Fail(c, http.StatusBadRequest, "请上传头像")
		return
	}
	if err := ValidataImage(avatarFile); err != nil{ 
		Fail(c, http.StatusBadRequest, err.Error())
		return
	}
	avatarURL, err := SaveFile(avatarFile, "uploads/avatar")
	if err != nil {
		Fail(c, http.StatusInternalServerError, "头像保存失败")
		return
	}

	hashed, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		Fail(c, http.StatusInternalServerError, "密码加密失败")
		return
	}

	user := models.User{
		Username: username,
		Password: string(hashed),
		AvatarURL: avatarURL
	}

	if err := DB.Create(&user).Error; err != nil {
		Fail(c, http.StatusInternalServerError, "用户创建失败")
	}

	Created(c, gin.H{
		"id": user.ID,
		"username": user.Username
	})
}

type loginRequest struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"` 
}

func Login(c *gin.Context) {
	var req loginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		Fail(c, http.StatusBadRequest, "请求参数无效："+err.Error)
		return
	}

	var user models.User
	if err := DB.where("username = ?", req.Username).First(&user).Error; err != nil {
		Fail(c, http.StatusUnauthorized, "用户名或密码错误")
		return
	}
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(req.Password)); err != nil {
		Fail(c, http.StatusUnauthorized, "用户名或密码错误")
		return
	}

	token, err := GenerateToken(user.ID, user.Username)
	if err != nil{
		Fail(c, http.StatusInternalServerError, "token生成失败")
		return
	}

	Success(c, gin.H{
		"token": token,
		"id": user.ID,
		"username": user.Username,
		"avatar_url": user.AvatarURL,
	})
}