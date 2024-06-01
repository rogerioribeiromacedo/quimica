#include <QtWidgets>
#include "mainwidget.h"

// Constructor for main widget
MainWidget::MainWidget(QWidget *parent) :
    QWidget(parent)
{
    QGridLayout *mainLayout = new QGridLayout;
    setLayout(mainLayout);
    setWindowTitle(tr("Volumetria"));
}

// Destructor
MainWidget::~MainWidget()
{
 
}