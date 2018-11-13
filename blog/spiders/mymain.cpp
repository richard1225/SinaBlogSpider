/*
*        Computer Graphics Course - Shenzhen University
*    Week 9 - Phong Reflectance Model (per-fragment shading)
* ============================================================
*
* - 本代码仅仅是参考代码，具体要求请参考作业说明，按照顺序逐步完成。
* - 关于配置OpenGL开发环境、编译运行，请参考第一周实验课程相关文档。
*/

#include "include/Angel.h"
#include "include/TriMesh.h"

#pragma comment(lib, "glew32.lib")

#include <cstdlib>
#include <iostream>

using namespace std;

GLuint programID;
GLuint vertexArrayID;
GLuint vertexBufferID;
GLuint vertexNormalID;
GLuint vertexIndexBuffer;

GLuint vPositionID;
GLuint vNormalID;
GLuint modelViewMatrixID;
GLuint modelViewProjMatrixID;
GLuint ProjMatrixID;
GLuint lightPosID;
GLuint shadID;
GLuint ShadID;

TriMesh* mesh = new TriMesh();
vec3 lightPos(0.0, 3.0, 3.0);

//////////////////////////////////////////////////////////////////////////
// 相机参数设置，因为本周不涉及相机观察变换和投影变换，所以将其设置为单位矩阵。

namespace Camera
{
    mat4 modelMatrix(1.0);
    mat4 viewMatrix(1.0);
    mat4 projMatrix(1.0);
}

//////////////////////////////////////////////////////////////////////////
// OpenGL 初始化

void init()
{
	glClearColor(0.75f, 0.75f, 0.75f, 1.0f);

	programID = InitShader("vshader_frag.glsl", "fshader_frag.glsl");

	// 从顶点着色器和片元着色器中获取变量的位置
	vPositionID = glGetAttribLocation(programID, "vPosition");
	vNormalID = glGetAttribLocation(programID, "vNormal");
	modelViewMatrixID = glGetUniformLocation(programID, "modelViewMatrix");
	ProjMatrixID = glGetUniformLocation(programID, "ProjMatrix");
	lightPosID = glGetUniformLocation(programID, "lightPos");
	shadID = glGetUniformLocation(programID, "shad");
	ShadID = glGetUniformLocation(programID, "Shad");

	// 读取外部三维模型
	mesh->read_off("sphere.off");

	vector<vec3f> vs = mesh->v();
	vector<vec3i> fs = mesh->f();
	vector<vec3f> ns;

	// TODO 计算球模型在每个顶点的法向量，并存储到ns数组中
	for (int i = 0; i < vs.size(); ++i) {
		ns.push_back(vs[i] - vec3(0.0, 0.0, 0.0));
	}

	// 生成VAO
	glGenVertexArrays(1, &vertexArrayID);
	glBindVertexArray(vertexArrayID);

	// 生成VBO，并绑定顶点数据
	glGenBuffers(1, &vertexBufferID);
	glBindBuffer(GL_ARRAY_BUFFER, vertexBufferID);
	glBufferData(GL_ARRAY_BUFFER, vs.size() * sizeof(vec3f), vs.data(), GL_STATIC_DRAW);

	// 生成VBO，并绑定法向量数据
	glGenBuffers(1, &vertexNormalID);
	glBindBuffer(GL_ARRAY_BUFFER, vertexNormalID);
	glBufferData(GL_ARRAY_BUFFER, ns.size() * sizeof(vec3f), ns.data(), GL_STATIC_DRAW);

	// 生成VBO，并绑定顶点索引
	glGenBuffers(1, &vertexIndexBuffer);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vertexIndexBuffer);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, fs.size() * sizeof(vec3i), fs.data(), GL_STATIC_DRAW);

	// OpenGL相应状态设置
	glEnable(GL_LIGHTING);
	glEnable(GL_DEPTH_TEST);
	glDepthFunc(GL_LESS);
	glEnable(GL_CULL_FACE);
}

//////////////////////////////////////////////////////////////////////////
// 渲染

void display()
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glUseProgram(programID);

	// TODO 计算相机观察矩阵和投影矩阵，并传入顶点着色器
	vec4 eye = vec4(0.0, 2.0, 2.0, 1.0);
	vec4 at = vec4(0.0, 0.0, 0.0, 1.0);
	vec4 up = vec4(0.0, 1.0, 0.0, 0.0);

	//设置视点
	mat4 modelViewMatrix = LookAt(eye, at, up);
	//设置透视投影
	mat4 ProjMatrix = Perspective(45.0, 1.0, 0.1, 100.0);


	glUniformMatrix4fv(modelViewMatrixID, 1, GL_TRUE, &modelViewMatrix[0][0]);
	glUniformMatrix4fv(ProjMatrixID, 1, GL_TRUE, &ProjMatrix[0][0]);

	// 将光源位置传入顶点着色器
	glUniform3fv(lightPosID, 1, &lightPos[0]);

	vec2 shadowp = vec2(0.0, 0.0);
	glUniform2fv(shadID, 1, shadowp);
	glUniform2fv(ShadID, 1, shadowp);

	glEnableVertexAttribArray(vPositionID);
	glBindBuffer(GL_ARRAY_BUFFER, vertexBufferID);
	glVertexAttribPointer(
		vPositionID,
		3,
		GL_FLOAT,
		GL_FALSE,
		0,
		(void*)0
	);

	glEnableVertexAttribArray(vNormalID);
	glBindBuffer(GL_ARRAY_BUFFER, vertexNormalID);
	glVertexAttribPointer(
		vNormalID,
		3,
		GL_FLOAT,
		GL_FALSE,
		0,
		(void*)0
	);

	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vertexIndexBuffer);

	glDrawElements(
		GL_TRIANGLES,
		int(mesh->f().size() * 3),
		GL_UNSIGNED_INT,
		(void*)0
	);


	//将光源点放入shadow矩阵进行构造，绘制阴影
	float lx = lightPos.x;
	float ly = lightPos.y;
	float lz = lightPos.z;
	mat4 shadowProjMatrix = mat4(-ly, 0.0, 0.0, 0.0,
								lx, 0.0, lz, 1.0,
								0.0, 0.0, -ly, 0.0,
								0.0, 0.0, 0.0, -ly);
	//更改当前绘制点的类型为阴影点
	shadowp = vec2(1.0, 1.0);
	glUniform2fv(shadID, 1, shadowp);
	glUniform2fv(ShadID, 1, shadowp);
	//更新相应的矩阵
	modelViewMatrix = modelViewMatrix * shadowProjMatrix;
	glUniformMatrix4fv(modelViewMatrixID, 1, GL_TRUE, &modelViewMatrix[0][0]);
	
	ProjMatrix * (0.0, -2.0,-2.0, 1.0);
	glUniformMatrix4fv(ProjMatrixID, 1, GL_TRUE, &ProjMatrix[0][0]);
	glDrawElements(GL_TRIANGLES, int(mesh->f().size() * 3), GL_UNSIGNED_INT, (void*)0);


	glDisableVertexAttribArray(vPositionID);
	glUseProgram(0);

	glutSwapBuffers();
}

//////////////////////////////////////////////////////////////////////////
// 重新设置窗口

void reshape(GLsizei w, GLsizei h)
{
    glViewport(0, 0, w, h);
}

//////////////////////////////////////////////////////////////////////////
// 鼠标响应函数

void mouse(int x, int y)
{
	// TODO 用鼠标控制光源的位置，并实时更新光照效果
}

//////////////////////////////////////////////////////////////////////////
// 键盘响应函数

void keyboard(unsigned char key, int x, int y)
{
	switch(key) 
	{
	case 033:	// ESC键 和 'q' 键退出游戏
		exit(EXIT_SUCCESS);
		break;
	case 'q':
		exit (EXIT_SUCCESS);
		break;
	case 'w':
		lightPos[1] += 1.0;
		break;
	case 's':
		lightPos[1] -= 1.0;
		break;
	case 'a':
		lightPos[0] -= 1.0;
		break;
	case 'd':
		lightPos[0] += 1.0;
		break;
	}
	glutPostRedisplay();
}

//////////////////////////////////////////////////////////////////////////

void idle(void)
{
	glutPostRedisplay();
}

//////////////////////////////////////////////////////////////////////////

void clean()
{
	glDeleteBuffers(1, &vertexBufferID);
	glDeleteProgram(programID);
	glDeleteVertexArrays(1, &vertexArrayID);

	if (mesh) {
		delete mesh;
		mesh = NULL;
	}
}

//////////////////////////////////////////////////////////////////////////

int main(int argc, char **argv)
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE);
	glutInitWindowSize(500, 500);
	glutCreateWindow("实验3_叶志杰_2015300091");

	glewInit();
	init();

	glutDisplayFunc(display);
	glutReshapeFunc(reshape);
	//glutMouseFunc(mouse);
	glutKeyboardFunc(keyboard);
	glutIdleFunc(idle);

	glutMainLoop();

	clean();

	return 0;
}