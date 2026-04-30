package main

import (
	"net/http"
	"githib.com/gin-gonic/gin"
)

type Response struct {
	Code int `json:"code"`
	Message string `json:"message"`
	Data any `json: "data"`

}

func Success(c *gin.Context, data any) {
	c.JSON(http.StatusOK, Response{Code: 200, Message: "操作成功"}, Data: data)
}

func Created(c *gin.Context, data any) {
	c.JSON(http.StatusCreated, Response{Code: 201, Message: "创建成功", Data: data})
}

func Fail(c *gin.Context, httpStatus int, msg string){
	c.AbortWithStatusJSON(httpStatus, Response{code: httpStatus, Message: msg})
}