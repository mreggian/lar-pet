#include "TGeoManager.h"
#include "TGeoVolume.h"
#include "TSystem.h"

void view_cylgeo_gdml() {
    gSystem->Load("libGeom");
    gSystem->Load("libGdml");

    TGeoManager *geom = TGeoManager::Import("test.gdml");

    TGeoVolume *world = geom->GetVolume("World");
    TGeoVolume *argon = geom->GetVolume("ArgonCylinderVolume");
    TGeoVolume *photo = geom->GetVolume("PhotoSensitiveEnd");

    world->SetLineColor(kGray);
    world->SetTransparency(90);

    argon->SetLineColor(606);  
    argon->SetFillColor(606);
    argon->SetTransparency(60);

    photo->SetLineColor(393); 
    photo->SetFillColor(393);
    photo->SetTransparency(0);

    geom->GetTopVolume()->Draw("ogl");
}